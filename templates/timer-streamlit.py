“””
streamlit_app.py
Performance-instrumented Streamlit app with real-time sidebar telemetry.
“””
import time
import functools
import streamlit as st
import pandas as pd
from typing import Callable, Any

# ══════════════════════════════════════════════════════════════════════════════

# TIMING INFRASTRUCTURE

# ══════════════════════════════════════════════════════════════════════════════

_CACHE_HIT_THRESHOLD_S: float = 0.005  # < 5ms → treat as a Streamlit cache hit

def _registry() -> list[dict]:
if “perf_log” not in st.session_state:
st.session_state[“perf_log”] = []
return st.session_state[“perf_log”]

def reset_registry() -> None:
“””
Call once at the top of main(). Clears the log so each rerun reflects
only the current execution — makes cache hit/miss detection unambiguous.
“””
st.session_state[“perf_log”] = []

def timed(label: str | None = None):
“””
Decorator — must sit ABOVE @st.cache_* in the stack.

```
    @timed("cache_data: fetch_orders")   ← fires on EVERY rerun
    @st.cache_data(ttl=300)              ← may skip the function body
    def fetch_orders(): ...

Cache hit  → elapsed ≈ 0 ms
Cache miss → elapsed = real cost

Placing @timed below @st.cache_* would only fire on misses,
hiding the very problem you're trying to diagnose.
"""
def decorator(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> Any:
        name = label or fn.__qualname__
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        _registry().append({
            "function":    name,
            "elapsed_s":   round(elapsed, 4),
            "is_cache_fn": any(k in name for k in ("cache_resource:", "cache_data:")),
        })
        return result
    return wrapper
return decorator
```

class timed_block:
“”“Context manager for timing render steps and inline blocks.”””

```
def __init__(self, label: str):
    self.label = label
    self._t0: float = 0.0

def __enter__(self):
    self._t0 = time.perf_counter()
    return self

def __exit__(self, *_):
    elapsed = time.perf_counter() - self._t0
    _registry().append({
        "function":    self.label,
        "elapsed_s":   round(elapsed, 4),
        "is_cache_fn": False,
    })
```

# ══════════════════════════════════════════════════════════════════════════════

# PERFORMANCE REPORT

# ══════════════════════════════════════════════════════════════════════════════

def _build_report_df() -> pd.DataFrame:
log = _registry()
if not log:
return pd.DataFrame()

```
raw     = pd.DataFrame(log)
total_s = raw["elapsed_s"].sum() or 1.0  # guard against division-by-zero

agg = (
    raw.groupby(["function", "is_cache_fn"], as_index=False)
       .agg(elapsed_s=("elapsed_s", "sum"))
       .sort_values("elapsed_s", ascending=False)
       .reset_index(drop=True)
)
agg["share_%"] = (agg["elapsed_s"] / total_s * 100).round(1)

def _status(row: pd.Series) -> str:
    if row["is_cache_fn"] and row["elapsed_s"] < _CACHE_HIT_THRESHOLD_S:
        return "✅ cached"
    if row["elapsed_s"] >= 1.0:
        return "🔴 slow"
    if row["elapsed_s"] >= 0.3:
        return "🟡 ok"
    return "🟢 fast"

agg["status"] = agg.apply(_status, axis=1)
agg.index += 1  # 1-based rank
return agg[["status", "function", "elapsed_s", "share_%"]]
```

def render_perf_sidebar(placeholder) -> None:
“”“Renders the full performance panel into the sidebar placeholder.”””
log = _registry()

```
with placeholder.container():
    if not log:
        st.caption("⏳ Waiting for first rerun…")
        return

    df      = _build_report_df()
    total_s = pd.DataFrame(log)["elapsed_s"].sum()

    # ── Summary metrics ────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    c1.metric("⏱ Total", f"{total_s:.3f}s")
    c2.metric("📍 Ops", len(df))

    st.divider()

    # ── Cache health ───────────────────────────────────────────────────
    cache_df = df[df["function"].str.contains(
        r"cache_resource:|cache_data:", regex=True, na=False
    )]
    if not cache_df.empty:
        st.markdown("##### 💾 Cache Health")
        st.caption("Hit = Streamlit returned a stored result (~0ms). "
                   "Miss = function body re-executed.")
        for _, row in cache_df.iterrows():
            fn_label = row["function"].split(": ", 1)[-1]
            elapsed  = f"{row['elapsed_s']:.4f}s"
            if row["status"] == "✅ cached":
                st.success(f"**{fn_label}** — hit `{elapsed}`")
            else:
                st.warning(f"**{fn_label}** — miss `{elapsed}`")
        st.divider()

    # ── Ranked breakdown ───────────────────────────────────────────────
    st.markdown("##### 📊 Ranked by Elapsed Time")
    display = (
        df.rename(columns={
            "status":    "Status",
            "function":  "Function",
            "elapsed_s": "Elapsed (s)",
            "share_%":   "Share %",
        })
    )
    st.dataframe(
        display.style
               .format({"Elapsed (s)": "{:.4f}", "Share %": "{:.1f}%"})
               .background_gradient(subset=["Elapsed (s)"], cmap="RdYlGn_r"),
        use_container_width=True,
        height=min(38 * (len(display) + 1) + 10, 480),
    )

    # ── Legend ─────────────────────────────────────────────────────────
    with st.expander("📖 Reading this report", expanded=False):
        st.markdown("""
```

|Icon    |Meaning                                    |
|:------:|:------------------------------------------|
|✅ cached|Cache hit — Streamlit skipped recomputation|
|⚠️ miss  |Cache miss — function body re-executed     |
|🔴 slow  |> 1.0s — highest priority to investigate   |
|🟡 ok    |0.3 – 1.0s — acceptable, monitor           |
|🟢 fast  |< 0.3s — no action needed                  |

**Share %** shows each operation’s fraction of total wall time.  
Timing resets on every Streamlit rerun.
“””)

# ══════════════════════════════════════════════════════════════════════════════

# CACHED RESOURCES

# ══════════════════════════════════════════════════════════════════════════════

@timed(“cache_resource: db_connection”)
@st.cache_resource
def get_db_connection():
time.sleep(0.5)
return “conn”

@timed(“cache_resource: sdk_client”)
@st.cache_resource
def get_sdk_client():
time.sleep(0.2)
return “client”

# ══════════════════════════════════════════════════════════════════════════════

# CACHED DATA

# ══════════════════════════════════════════════════════════════════════════════

@timed(“cache_data: fetch_main_dataset”)
@st.cache_data(ttl=300)
def fetch_main_dataset(_conn) -> pd.DataFrame:
time.sleep(1.0)
return pd.DataFrame({“A”: [1, 2, 3], “B”: [10, 20, 30], “C”: [“x”, “y”, “z”]})

@timed(“cache_data: fetch_lookup_table”)
@st.cache_data(ttl=300)
def fetch_lookup_table(_client) -> pd.DataFrame:
time.sleep(0.3)
return pd.DataFrame({“ID”: [1, 2], “Label”: [“Alpha”, “Beta”]})

# ══════════════════════════════════════════════════════════════════════════════

# DATA TRANSFORMS

# ══════════════════════════════════════════════════════════════════════════════

@timed(“transform: add_checkbox_column”)
def add_checkbox_column(df: pd.DataFrame) -> pd.DataFrame:
df = df.copy()
df.insert(0, “select”, False)
return df

@timed(“transform: filter_selected_rows”)
def filter_selected_rows(df: pd.DataFrame) -> pd.DataFrame:
return df[df[“select”]].drop(columns=[“select”])

# ══════════════════════════════════════════════════════════════════════════════

# SUBMISSION

# ══════════════════════════════════════════════════════════════════════════════

@timed(“submit: send_to_target”)
def send_to_target(client, payload: pd.DataFrame) -> bool:
time.sleep(0.8)
return True

@timed(“sdk: close_application”)
def close_application(client) -> None:
time.sleep(0.1)

# ══════════════════════════════════════════════════════════════════════════════

# APP

# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
# Must be the first Streamlit call in the script
st.set_page_config(
page_title=“My App”,
page_icon=“📊”,
layout=“wide”,
)

```
# Fresh timing slate for this rerun
reset_registry()

# ── Sidebar shell (content injected at end of rerun) ──────────────────
with st.sidebar:
    st.title("⏱ Performance Monitor")
    st.caption(
        "Resets on every Streamlit rerun. "
        "Cache hits show ~0ms — misses show real execution time."
    )
    st.divider()
    perf_placeholder = st.empty()

# ── Resources (measured but not displayed as a section) ───────────────
conn   = get_db_connection()
client = get_sdk_client()

# ── Page header ───────────────────────────────────────────────────────
st.title("📊 My Streamlit App")
st.caption("Select rows from the table below and submit them to the target system.")

# ── Section 1: Data ───────────────────────────────────────────────────
st.header("1 · Data", divider="gray")
st.caption(
    "Loaded from Redshift via SDK. Cached for 5 minutes — "
    "check **Cache Health** in the sidebar to confirm hits vs. misses."
)

with timed_block("render: data fetch + join"):
    df      = fetch_main_dataset(conn)
    lookups = fetch_lookup_table(client)  # noqa: F841

# ── Section 2: Row Selection ──────────────────────────────────────────
st.header("2 · Select Rows", divider="gray")
st.caption("Toggle **Select** on any rows to include them in the submission.")

df = add_checkbox_column(df)

with timed_block("render: data_editor display"):
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        column_config={
            "select": st.column_config.CheckboxColumn(
                "Select", help="Include this row in submission", default=False
            )
        },
    )

# ── Section 3: Submit ─────────────────────────────────────────────────
st.header("3 · Submit", divider="gray")
st.caption("Sends selected rows to the target system via SDK.")

with st.form("submit_form"):
    submitted = st.form_submit_button("🚀  Submit Selected Rows", type="primary")

if submitted:
    with timed_block("render: pre-submit filter"):
        payload = filter_selected_rows(edited_df)

    if payload.empty:
        st.warning("No rows selected — use the checkboxes above to pick at least one.")
    else:
        with st.spinner(f"Sending {len(payload)} row(s)…"):
            success = send_to_target(client, payload)

        if success:
            st.success(f"✅ {len(payload)} row(s) submitted successfully.")
            close_application(client)

# ── Render sidebar at end of every rerun ─────────────────────────────
render_perf_sidebar(perf_placeholder)
```

if **name** == “**main**”:
main()