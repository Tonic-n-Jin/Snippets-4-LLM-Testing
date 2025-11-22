"""
cleaning/engine.py

Polars-based, YAML-driven, DRY data cleaning engine.

Key ideas:
- Rules are declared in YAML and validated via Pydantic.
- Polars LazyFrame is used for performance & scalability.
- Pandera enforces input/output contracts (schemas defined elsewhere).
- Structlog provides structured, correlation-id-aware logging.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

import polars as pl
import structlog
import yaml
from pydantic import BaseModel, Field, validator

try:
    from pandera import check_io  # type: ignore
except ImportError:
    # Optional: if Pandera isn't available, define a no-op decorator
    def check_io(*_, **__):  # type: ignore
        def decorator(func):
            return func

        return decorator


logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Pydantic models for YAML-driven rules
# ---------------------------------------------------------------------------


class ColumnSchema(BaseModel):
    dtype: str
    nullable: bool = True
    coerce: bool = False
    checks: Dict[str, Any] = Field(default_factory=dict)


class NumericCleaningRules(BaseModel):
    default_strategy: str = "median"  # "median" | "mean" | "constant"
    default_fill_value: Optional[float] = None
    high_missing_threshold: float = 0.3
    use_knn_if_above: float = 0.15  # not implemented here, reserved
    outlier_strategy: Optional[str] = "clip_iqr_1_5"

    @validator("high_missing_threshold", "use_knn_if_above")
    def _check_threshold(cls, v: float) -> float:
        if not 0 <= v <= 1:
            raise ValueError("thresholds must be in [0, 1]")
        return v


class CategoricalCleaningRules(BaseModel):
    default_strategy: str = "mode"  # "mode" | "constant"
    default_fill_value: Optional[str] = None
    high_missing_strategy: str = "new_category"  # "new_category" | "drop"
    new_category_name: str = "MISSING"
    high_cardinality_threshold: int = 100
    rare_category_min_pct: float = 0.01
    rare_strategy_group_as_other: bool = True

    @validator("rare_category_min_pct")
    def _check_pct(cls, v: float) -> float:
        if not 0 <= v <= 1:
            raise ValueError("rare_category_min_pct must be in [0, 1]")
        return v


class DatetimeRule(BaseModel):
    column: str
    coerce: bool = True
    fill_strategy: Optional[str] = None  # "ffill" | "bfill" | None


class CleaningConfig(BaseModel):
    drop_columns_if_missing_gt: float = 0.7
    drop_rows_if_missing_gt: float = 0.5

    numeric: NumericCleaningRules = NumericCleaningRules()
    categorical: CategoricalCleaningRules = CategoricalCleaningRules()
    datetime: List[DatetimeRule] = Field(default_factory=list)

    @validator("drop_columns_if_missing_gt", "drop_rows_if_missing_gt")
    def _check_missing_threshold(cls, v: float) -> float:
        if not 0 <= v <= 1:
            raise ValueError("missing thresholds must be in [0, 1]")
        return v


class CleaningRules(BaseModel):
    table: str
    valid_from: Optional[str] = None
    rule_version: Optional[int] = 1

    schema: Dict[str, ColumnSchema]
    cleaning: CleaningConfig

    class Config:
        extra = "forbid"


def load_rules(path: Path) -> CleaningRules:
    """Load CleaningRules from a YAML file."""
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return CleaningRules(**raw)


# ---------------------------------------------------------------------------
# Core Cleaning Engine
# ---------------------------------------------------------------------------


@dataclass
class DataCleaner:
    rules: CleaningRules
    correlation_id: Optional[str] = None

    # external schemas for Pandera are assumed defined elsewhere
    schema_in: Any = None
    schema_out: Any = None

    # internal audit info (collected as we go)
    _audit: Dict[str, Any] = field(default_factory=dict, init=False)

    def _log(self, **kwargs: Any) -> structlog.BoundLogger:
        base = {"corr_id": self.correlation_id, "table": self.rules.table}
        base.update(kwargs)
        return logger.bind(**base)

    # ------------------------------------------------------------------- #
    # Pandera integration (optional)                                      #
    # ------------------------------------------------------------------- #

    def _check_io_decorator(self):
        """Return a check_io decorator instance or a no-op if schemas not provided."""
        if self.schema_in is not None and self.schema_out is not None:
            return check_io(df_in=self.schema_in, df_out=self.schema_out)
        return check_io()  # type: ignore[func-returns-value]

    # ------------------------------------------------------------------- #
    # Public API                                                          #
    # ------------------------------------------------------------------- #

    def transform(self, df: pl.LazyFrame) -> pl.LazyFrame:
        """
        Main cleaning entrypoint.

        The @check_io decorator is dynamically attached to preserve
        Pandera contracts while allowing LazyFrame-based implementation.
        """

        @self._check_io_decorator()
        def _inner_transform(df_in: pl.LazyFrame) -> pl.LazyFrame:
            log = self._log(stage="start")
            log.info("cleaning_start")

            rows_in = None  # we lazily infer later

            df_clean = df_in

            # 1. Coerce dtypes where configured
            df_clean = self._coerce_dtypes(df_clean)

            # 2. Drop high-missing columns / rows
            df_clean = self._drop_high_missing(df_clean)

            # 3. Numeric pipeline
            df_clean = self._clean_numeric(df_clean)

            # 4. Categorical pipeline
            df_clean = self._clean_categorical(df_clean)

            # 5. Datetime pipeline
            df_clean = self._clean_datetime(df_clean)

            # 6. Attach audit metadata
            df_clean = df_clean.with_columns(
                pl.lit(self.correlation_id).alias("_cleaning_run_id"),
                pl.lit(self.rules.rule_version).alias("_cleaning_rule_version"),
                pl.lit(self.rules.table).alias("_cleaning_table"),
            )

            # 7. Collect minimal stats for audit (rows_in/out, etc.)
            stats = df_clean.select(pl.len().alias("_rows_out")).collect()
            rows_out = int(stats["_rows_out"][0])
            self._audit.setdefault("rows_out", rows_out)

            log.info(
                "cleaning_complete",
                audit=self._audit,
            )
            return df_clean

        return _inner_transform(df)

    # ------------------------------------------------------------------- #
    # Step 0: Coerce dtypes according to schema                           #
    # ------------------------------------------------------------------- #

    def _coerce_dtypes(self, df: pl.LazyFrame) -> pl.LazyFrame:
        """Cast columns to configured dtypes where coerce=True."""
        schema_rules = self.rules.schema
        exprs: List[pl.Expr] = []
        existing_cols = df.schema  # name -> dtype

        for col_name, col_schema in schema_rules.items():
            if col_name not in existing_cols:
                continue
            if not col_schema.coerce:
                continue

            pl_dtype = self._to_polars_dtype(col_schema.dtype)
            exprs.append(pl.col(col_name).cast(pl_dtype))

        if not exprs:
            return df

        log = self._log(stage="coerce_dtypes")
        log.info("dtype_coercion", columns=[e.meta.output_name() for e in exprs])

        return df.with_columns(exprs)

    @staticmethod
    def _to_polars_dtype(dtype_str: str) -> pl.DataType:
        """Map YAML dtype string to Polars dtype."""
        mapping = {
            "string": pl.Utf8,
            "float64": pl.Float64,
            "float32": pl.Float32,
            "int64": pl.Int64,
            "int32": pl.Int32,
            "bool": pl.Boolean,
            "datetime": pl.Datetime,
            "date": pl.Date,
        }
        if dtype_str not in mapping:
            raise ValueError(f"Unsupported dtype in rules: {dtype_str}")
        return mapping[dtype_str]

    # ------------------------------------------------------------------- #
    # Step 1: Drop high-missing columns and rows                          #
    # ------------------------------------------------------------------- #

    def _drop_high_missing(self, df: pl.LazyFrame) -> pl.LazyFrame:
        cfg = self.rules.cleaning
        log = self._log(stage="drop_high_missing")

        # Column-wise missing fraction
        # We can compute null_count per column + length in one tiny summary frame.
        cols = list(df.schema.keys())
        null_exprs = [pl.col(c).null_count().alias(c) for c in cols]
        stats_lf = df.select(null_exprs + [pl.len().alias("__len")])
        stats = stats_lf.collect()
        total_rows = stats["__len"][0] if "__len" in stats.columns else 0

        if total_rows == 0:
            self._audit["rows_in"] = 0
            self._audit["rows_out"] = 0
            return df  # nothing to do

        self._audit["rows_in"] = int(total_rows)

        col_null_counts = {c: int(stats[c][0]) for c in cols}
        col_missing_frac = {c: col_null_counts[c] / total_rows for c in cols}

        drop_cols = [
            c
            for c, frac in col_missing_frac.items()
            if frac > cfg.drop_columns_if_missing_gt
        ]
        keep_cols = [c for c in cols if c not in drop_cols]

        self._audit["cols_dropped_high_missing"] = drop_cols

        if drop_cols:
            log.info(
                "drop_columns_high_missing",
                threshold=cfg.drop_columns_if_missing_gt,
                columns=drop_cols,
            )

        df = df.select(keep_cols)

        # Row-wise missing fraction
        # Count nulls horizontally on remaining columns.
        row_nulls_expr = pl.all().null_count().keep_name().sum_horizontal().alias("_row_nulls")
        df = df.with_columns(row_nulls_expr)

        df = df.with_columns(
            (pl.col("_row_nulls") / pl.len()).alias("_row_missing_frac")
        ).filter(
            pl.col("_row_missing_frac") <= cfg.drop_rows_if_missing_gt
        ).drop(
            ["_row_nulls", "_row_missing_frac"]
        )

        self._audit["drop_rows_if_missing_gt"] = cfg.drop_rows_if_missing_gt
        return df

    # ------------------------------------------------------------------- #
    # Step 2: Numeric cleaning                                            #
    # ------------------------------------------------------------------- #

    def _clean_numeric(self, df: pl.LazyFrame) -> pl.LazyFrame:
        cfg = self.rules.cleaning.numeric
        log = self._log(stage="numeric")

        # Identify numeric columns from schema configuration
        numeric_cols = [
            name
            for name, col_schema in self.rules.schema.items()
            if col_schema.dtype.startswith("float") or col_schema.dtype.startswith("int")
            if name in df.schema
        ]

        if not numeric_cols:
            return df

        # Imputation according to default_strategy
        impute_exprs: List[pl.Expr] = []
        for col in numeric_cols:
            if cfg.default_strategy == "median":
                impute_exprs.append(
                    pl.col(col).fill_null(pl.col(col).median())
                )
            elif cfg.default_strategy == "mean":
                impute_exprs.append(
                    pl.col(col).fill_null(pl.col(col).mean())
                )
            elif cfg.default_strategy == "constant":
                if cfg.default_fill_value is None:
                    raise ValueError(
                        f"default_fill_value must be set for constant strategy (numeric col={col})"
                    )
                impute_exprs.append(
                    pl.col(col).fill_null(cfg.default_fill_value)
                )
            else:
                raise ValueError(f"Unsupported numeric imputation strategy: {cfg.default_strategy}")

        df = df.with_columns(impute_exprs)
        self._audit["numeric_imputation_strategy"] = cfg.default_strategy
        log.info("numeric_imputation", columns=numeric_cols, strategy=cfg.default_strategy)

        # Outlier handling via IQR clipping (if configured)
        if cfg.outlier_strategy and cfg.outlier_strategy.startswith("clip_iqr"):
            # parse factor, e.g. "clip_iqr_1_5"
            parts = cfg.outlier_strategy.split("_")
            factor = 1.5
            try:
                factor = float(parts[-2]) / float(parts[-1])
            except Exception:
                pass

            # Compute Q1, Q3, IQR and clip per column
            for col in numeric_cols:
                quantiles_lf = df.select(
                    pl.col(col).quantile(0.25).alias("q1"),
                    pl.col(col).quantile(0.75).alias("q3"),
                )
                q_df = quantiles_lf.collect()
                q1 = q_df["q1"][0]
                q3 = q_df["q3"][0]
                iqr = q3 - q1
                lower = q1 - factor * iqr
                upper = q3 + factor * iqr

                df = df.with_columns(
                    pl.col(col).clip(lower, upper)
                )

            self._audit["numeric_outlier_strategy"] = cfg.outlier_strategy
            log.info(
                "numeric_outlier_clipping",
                columns=numeric_cols,
                strategy=cfg.outlier_strategy,
            )

        return df

    # ------------------------------------------------------------------- #
    # Step 3: Categorical cleaning                                       #
    # ------------------------------------------------------------------- #

    def _clean_categorical(self, df: pl.LazyFrame) -> pl.LazyFrame:
        cfg = self.rules.cleaning.categorical
        log = self._log(stage="categorical")

        cat_cols = [
            name
            for name, col_schema in self.rules.schema.items()
            if col_schema.dtype == "string" and name in df.schema
        ]

        if not cat_cols:
            return df

        # Imputation: mode or constant
        for col in cat_cols:
            if cfg.default_strategy == "mode":
                mode_lf = df.select(pl.col(col).mode().alias("mode"))
                mode_df = mode_lf.collect()
                if mode_df.height == 0:
                    continue
                mode_val = mode_df["mode"][0]
                df = df.with_columns(
                    pl.col(col).fill_null(mode_val)
                )
            elif cfg.default_strategy == "constant":
                if cfg.default_fill_value is None:
                    raise ValueError(
                        f"default_fill_value must be set for constant strategy (categorical col={col})"
                    )
                df = df.with_columns(
                    pl.col(col).fill_null(cfg.default_fill_value)
                )
            else:
                raise ValueError(f"Unsupported categorical imputation strategy: {cfg.default_strategy}")

        self._audit["categorical_imputation_strategy"] = cfg.default_strategy
        log.info(
            "categorical_imputation",
            columns=cat_cols,
            strategy=cfg.default_strategy,
        )

        # High-cardinality & rare-category handling (simple grouping to 'OTHER')
        for col in cat_cols:
            freq_lf = df.select(pl.col(col).value_counts())
            freq_df = freq_lf.collect()
            if freq_df.height == 0 or "counts" not in freq_df.columns:
                continue

            total = freq_df["counts"].sum()
            freq_df = freq_df.with_columns(
                (pl.col("counts") / total).alias("pct")
            )
            # Identify rare categories
            rare_cats = (
                freq_df.filter(pl.col("pct") < cfg.rare_category_min_pct)
                .select("column_0")[  # column name depends on polars version; adjust if needed
                0
                ]
                .to_list()
            )

            if cfg.rare_strategy_group_as_other and rare_cats:
                df = df.with_columns(
                    pl.when(pl.col(col).is_in(rare_cats))
                    .then("OTHER")
                    .otherwise(pl.col(col))
                    .alias(col)
                )

        self._audit["categorical_rare_threshold"] = cfg.rare_category_min_pct
        return df

    # ------------------------------------------------------------------- #
    # Step 4: Datetime cleaning                                          #
    # ------------------------------------------------------------------- #

    def _clean_datetime(self, df: pl.LazyFrame) -> pl.LazyFrame:
        dt_rules = self.rules.cleaning.datetime
        if not dt_rules:
            return df

        log = self._log(stage="datetime")

        for rule in dt_rules:
            col = rule.column
            if col not in df.schema:
                continue

            expr = pl.col(col)
            if rule.coerce:
                expr = expr.str.strptime(pl.Datetime, strict=False)

            df = df.with_columns(expr.alias(col))

            if rule.fill_strategy == "ffill":
                df = df.with_columns(pl.col(col).forward_fill())
            elif rule.fill_strategy == "bfill":
                df = df.with_columns(pl.col(col).backward_fill())

        log.info(
            "datetime_cleaning",
            columns=[r.column for r in dt_rules],
        )
        return df


# ---------------------------------------------------------------------------
# Example usage (conceptual)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # This is a small conceptual example; in real usage, you'd scan Parquet/Delta.
    sample_rules_path = Path("rules/transaction_features.yaml")
    rules = load_rules(sample_rules_path)

    cleaner = DataCleaner(rules=rules, correlation_id="run-2025-03-15T10:00Z")

    # Example input (eager -> lazy)
    df = pl.DataFrame(
        {
            "user_id": ["u1", "u2", "u3", None],
            "amount": [100.0, None, -5.0, 50.0],
            "country_code": ["US", None, "DE", "US"],
            "event_ts": ["2025-01-01 10:00:00", None, "2025-01-02 11:00:00", "invalid"],
        }
    ).lazy()

    cleaned_lf = cleaner.transform(df)
    cleaned_df = cleaned_lf.collect()
    print(cleaned_df)
