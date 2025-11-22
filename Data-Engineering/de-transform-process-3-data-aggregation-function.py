import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def aggregate_to_user_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates an enriched order DataFrame to create a user-level
    summary analytical view.
    """
    if df.empty or 'user_id' not in df.columns:
        logging.warning("Cannot aggregate: DataFrame is empty or missing 'user_id'.")
        return pd.DataFrame()

    logging.info(f"Aggregating {len(df)} records to user summary...")

    # Define the aggregations using NamedAgg for clarity and new column names
    agg_rules = {
        'total_spend': pd.NamedAgg(column='order_total', aggfunc='sum'),
        'total_orders': pd.NamedAgg(column='order_id', aggfunc='nunique'),
        'first_order_date': pd.NamedAgg(column='order_date', aggfunc='min'),
        'last_order_date': pd.NamedAgg(column='order_date', aggfunc='max'),
        'countries': pd.NamedAgg(column='country', aggfunc='unique')
    }
    
    # Run the groupby and apply the aggregation rules
    user_summary = df.groupby('user_id').agg(**agg_rules).reset_index()
    
    logging.info(f"Created summary for {len(user_summary)} users.")
    return user_summary

# --- Example Usage ---
# (Assumes 'enriched_data' from the previous example)
enriched_data = pd.DataFrame({
    'order_id': ['o1', 'o2', 'o3', 'o4'],
    'user_id': ['u1', 'u2', 'u1', 'u2'],
    'order_total': [50, 200, 150, 30],
    'order_date': pd.to_datetime(['2025-11-17', '2025-11-17', '2025-11-18', '2025-11-19']),
    'country': ['USA', 'CAN', 'USA', 'CAN']
})

user_summary_data = aggregate_to_user_summary(enriched_data)
print(user_summary_data)
