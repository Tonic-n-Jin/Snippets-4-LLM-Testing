from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score

class ClusteringProblem:
    def __init__(self, X, business_context):
        self.X = X
        self.context = business_context
        
    def determine_optimal_clusters(self):
        """Find optimal number of clusters"""
        scores = {
            'silhouette': [],
            'inertia': [],
            'davies_bouldin': []
        }
        
        K = range(2, min(10, len(self.X) // 30))
        
        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(self.X)
            
            scores['silhouette'].append(
                silhouette_score(self.X, labels)
            )
            scores['inertia'].append(kmeans.inertia_)
            scores['davies_bouldin'].append(
                davies_bouldin_score(self.X, labels)
            )
        
        # Elbow method + silhouette
        optimal_k = self.find_elbow(scores['inertia'])
        
        return optimal_k, scores
    
    def profile_clusters(self, labels):
        """Create business profiles for each cluster"""
        profiles = {}
        
        for cluster_id in np.unique(labels):
            mask = labels == cluster_id
            cluster_data = self.X[mask]
            
            profiles[f'Cluster_{cluster_id}'] = {
                'size': mask.sum(),
                'percentage': mask.mean() * 100,
                'centroid': cluster_data.mean(),
                'key_features': self.identify_key_features(cluster_data)
            }
        
        return profiles