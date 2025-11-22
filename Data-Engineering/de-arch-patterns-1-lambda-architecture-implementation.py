class LambdaArchitecture:
    def __init__(self):
        self.batch_layer = BatchProcessingLayer()
        self.speed_layer = StreamProcessingLayer()
        self.serving_layer = ServingLayer()
    
    def process(self, data):
        """Parallel processing through batch and speed layers"""
        # Batch layer: Complete and accurate but slow
        batch_views = self.batch_layer.compute_views(data)
        
        # Speed layer: Fast but approximate
        real_time_views = self.speed_layer.process_stream(data)
        
        # Serving layer: Merge batch and real-time views
        return self.serving_layer.query(
            batch_views, 
            real_time_views
        )
    
    def recompute_batch_views(self):
        """Periodic batch recomputation for accuracy"""
        historical_data = self.get_all_historical_data()
        self.batch_layer.recompute(historical_data)