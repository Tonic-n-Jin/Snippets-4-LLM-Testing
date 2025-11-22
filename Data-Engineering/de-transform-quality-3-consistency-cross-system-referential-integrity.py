import logging
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ConsistencyValidator:
    """
    Checks consistency between different systems.
    Example: Ensures every 'user_id' in the 'payments' system
    also exists in the 'users' (SSO) system.
    """
    def __init__(self, users_db_conn_str: str, payments_db_conn_str: str):
        self.users_engine = create_engine(users_db_conn_str)
        self.payments_engine = create_engine(payments_db_conn_str)

    def _get_ids_as_set(self, engine, query: str) -> set:
        """Runs a query and returns the first column's results as a set."""
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return {row[0] for row in result}

    def check_referential_integrity(self, 
                                     users_table="users", users_id_col="id",
                                     payments_table="transactions", payments_user_col="user_id"):
        """
        Finds 'orphan' records in the payments table that don't have a
        corresponding user in the users table.
        """
        logging.info("Checking referential integrity between payments and users...")
        
        # 1. Get all unique user IDs from the 'child' (payments) table
        payments_query = f"SELECT DISTINCT {payments_user_col} FROM {payments_table}"
        payment_user_ids = self._get_ids_as_set(self.payments_engine, payments_query)
        
        # 2. Get all valid user IDs from the 'parent' (users) table
        users_query = f"SELECT {users_id_col} FROM {users_table}"
        master_user_ids = self._get_ids_as_set(self.users_engine, users_query)
        
        # 3. Find the difference (the inconsistent orphans)
        orphan_ids = payment_user_ids - master_user_ids
        
        if not orphan_ids:
            logging.info(f"Check passed: All {len(payment_user_ids)} users in payments are consistent with users table.")
            return {"is_consistent": True, "orphan_count": 0, "orphan_examples": []}
        else:
            logging.warning(f"Check FAILED: Found {len(orphan_ids)} orphan user IDs in payments table.")
            return {
                "is_consistent": False,
                "orphan_count": len(orphan_ids),
                "orphan_examples": list(orphan_ids)[:10] # Show first 10
            }
