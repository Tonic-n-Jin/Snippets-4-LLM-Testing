import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def enrich_order_data(orders_df: pd.DataFrame, user_lookup_df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches order data by joining user data and calculating new features.
    """
    logging.info(f"Enriching {len(orders_df)} order records...")
    
    # 1. Join datasets (add context)
    enriched_df = pd.merge(
        orders_df, 
        user_lookup_df, 
        on="user_id", 
        how="left"
    )
    # Handle joins that didn't match
    enriched_df['country'] = enriched_df['country'].fillna('Unknown')
    logging.info("Joined with user lookup data.")

    # 2. Calculate new metrics/features (e.g., high-value flag)
    enriched_df['is_high_value'] = enriched_df['order_total'] > 100
    
    # 3. Feature extraction (e.g., from timestamp)
    enriched_df['order_date'] = pd.to_datetime(enriched_df['order_timestamp'])
    enriched_df['order_day_of_week'] = enriched_df['order_date'].dt.day_name()
    logging.info("Calculated 'is_high_value' and date features.")
    
    return enriched_df

# --- Example Usage ---
orders = pd.DataFrame({
    'order_id': ['o1', 'o2', 'o3'],
    'user_id': ['u1', 'u2', 'u1'],
    'order_total': [50, 200, 150],
    'order_timestamp': ['2025-11-17T10:00:00', '2025-11-17T11:00:00', '2025-11-17T12:00:00']
})

user_lookup = pd.DataFrame({
    'user_id': ['u1', 'u2', 'u3'],
    'country': ['USA', 'CAN', 'MEX']
})

enriched_data = enrich_order_data(orders, user_lookup)
print(enriched_data)
