import pandas as pd
import pandera as pa
from pandera.errors import SchemaErrors

# Pandera provides a declarative way to define and validate data schemas.
# This ensures all values are accurate according to business rules.

# 1. Define the validation schema
user_schema = pa.DataFrameSchema(
    columns={
        "user_id": pa.Column(
            pa.String, 
            checks=pa.Check.str_startswith("u-"), 
            nullable=False,
            unique=True
        ),
        "email": pa.Column(
            pa.String, 
            checks=pa.Check.str_matches(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
            nullable=False
        ),
        "age": pa.Column(
            pa.Int, 
            checks=pa.Check.in_range(min_value=18, max_value=120),
            nullable=True
        ),
        "account_status": pa.Column(
            pa.String,
            checks=pa.Check.isin(["active", "pending", "disabled", "expired"]),
            nullable=False
        )
    },
    # Check that if age is null, status must be 'pending'
    checks=pa.Check(
        lambda df: ~df["age"].isna() | (df["account_status"] == "pending"),
        name="age_null_only_if_pending"
    )
)

# 2. Load some sample data
data = pd.DataFrame({
    "user_id": ["u-123", "u-456", "u-789", "u-101"],
    "email": ["alice@example.com", "bob@test.com", "invalid-email", "charlie@web.com"],
    "age": [25, 42, 30, 999],
    "account_status": ["active", "pending", "active", "disabled"]
})

# 3. Run the validation
try:
    validated_data = user_schema.validate(data, lazy=True)
    print("Data is accurate and valid.")
except SchemaErrors as err:
    print("Data accuracy check failed:")
    # err.failure_cases provides a detailed report of all failures
    print(err.failure_cases)
