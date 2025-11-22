class HybridStorage:
    def __init__(self):
        self.data_lake = S3Storage()
        self.data_warehouse = SnowflakeWarehouse()
        self.cache = RedisCache()
    
    def store_data(self, data, access_pattern):
        """Route data to appropriate storage tier"""
        if access_pattern == 'archival':
            # Cold storage in data lake
            return self.data_lake.store(
                data, 
                storage_class='GLACIER'
            )
        elif access_pattern == 'analytical':
            # Structured storage in warehouse
            return self.data_warehouse.load(
                data,
                clustering_keys=['date', 'region']
            )
        elif access_pattern == 'real_time':
            # Hot storage in cache
            return self.cache.set(
                data,
                ttl=3600  # 1 hour TTL
            )
    
    def query_data(self, query):
        """Federated query across storage layers"""
        if self.cache.exists(query.key):
            return self.cache.get(query.key)
        elif query.is_structured():
            return self.data_warehouse.query(query)
        else:
            return self.data_lake.scan(query)