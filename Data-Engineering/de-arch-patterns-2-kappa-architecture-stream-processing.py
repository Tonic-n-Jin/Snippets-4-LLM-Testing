class KappaArchitecture:
    def __init__(self, kafka_config):
        self.stream_processor = StreamProcessor(kafka_config)
        self.state_store = StateStore()
    
    def process_event_stream(self, topic):
        """Single stream processing path"""
        @self.stream_processor.process(topic)
        def handle_event(event):
            # All processing happens in streaming layer
            transformed = self.transform(event)
            aggregated = self.aggregate(transformed)
            
            # Update state store
            self.state_store.update(aggregated)
            
            # Emit results
            return aggregated
    
    def replay_from_beginning(self):
        """Reprocess entire stream from beginning"""
        self.stream_processor.seek_to_beginning()
        self.state_store.clear()
        self.stream_processor.start()