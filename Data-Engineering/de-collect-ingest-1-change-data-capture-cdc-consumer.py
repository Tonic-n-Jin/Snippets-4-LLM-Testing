import faust
import logging

# ---
# This example shows the CONSUMER side of CDC.
# It assumes a tool like Debezium is running, monitoring a database 
# (e.g., 'customers' table) and publishing changes to a Kafka topic 
# named 'db.public.customers'.
# ---

logging.basicConfig(level=logging.INFO)

# 1. Define the Faust app and Kafka broker
app = faust.App('cdc-processor', broker='kafka://localhost:9092')

# 2. Define the complex structure of a Debezium CDC event
# We only map the fields we care about. 'before' is null on CREATE.
class DebeziumPayload(faust.Record):
    before: dict | None
    after: dict | None
    source: dict
    op: str # 'c' = create, 'u' = update, 'd' = delete, 'r' = read
    ts_ms: int

# 3. Define the Kafka topic, using our DebeziumPayload type
cdc_topic = app.topic('db.public.customers', value_type=DebeziumPayload)

class ChangeHandler:
    """A modular class to handle applying changes to a downstream system."""
    
    def handle_create(self, record: dict):
        # Logic to insert the new record into a data warehouse, search index, etc.
        logging.info(f"CREATE: User {record.get('id')}, Email: {record.get('email')}")
        # e.g., db.execute("INSERT INTO dim_users ...", record)

    def handle_update(self, before: dict, after: dict):
        # Logic to update an existing record
        logging.info(f"UPDATE: User {after.get('id')}, Old Email: {before.get('email')}, New Email: {after.get('email')}")
        # e.g., db.execute("UPDATE dim_users SET email = ... WHERE id = ...", after)

    def handle_delete(self, record: dict):
        # Logic to soft-delete or hard-delete a record
        logging.warning(f"DELETE: User {record.get('id')}")
        # e.g., db.execute("UPDATE dim_users SET is_active = false WHERE id = ...", record)

# Instantiate our handler (could be passed dependencies)
handler = ChangeHandler()

# 4. Define the Faust agent to process the CDC stream
@app.agent(cdc_topic)
async def process_cdc_stream(events):
    """
    Consumes the CDC event stream and routes events based on operation type.
    """
    async for event in events:
        try:
            op = event.op
            if op == 'c':
                handler.handle_create(event.after)
            elif op == 'u':
                handler.handle_update(event.before, event.after)
            elif op == 'd':
                handler.handle_delete(event.before)
            elif op == 'r':
                # 'r' is a snapshot read, treat as a create
                handler.handle_create(event.after)
        except Exception as e:
            logging.error(f"Failed to process event {event.source.get('txId')}: {e}")
            # Optionally send to a dead-letter-queue

if __name__ == "__main__":
    # Run with: faust -A cdc_app worker -l info
    app.main()
