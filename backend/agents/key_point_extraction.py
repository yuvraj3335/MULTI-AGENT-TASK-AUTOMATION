from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
import logging

logger = logging.getLogger(__name__)

class KeyPointExtractionAgent:
    def __init__(self):
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("SentenceTransformer model loaded")

    def extract_key_points(self, transcription):
        logger.info("Extracting key points from transcription")
        sentences = [s.strip() for s in transcription.split('. ') if s.strip()]
        if len(sentences) < 2:
            logger.info("Transcription too short, returning single key point")
            return [{"text": transcription, "cluster_id": 0, "embedding": self.sentence_model.encode([transcription])[0].tolist()}]
        embeddings = self.sentence_model.encode(sentences)
        num_clusters = min(5, len(sentences) // 2 + 1)
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(embeddings)
        key_points = []
        for i in range(num_clusters):
            cluster_indices = [j for j, label in enumerate(kmeans.labels_) if label == i]
            if cluster_indices:
                cluster_embeddings = embeddings[cluster_indices]
                centroid = kmeans.cluster_centers_[i]
                distances = [np.linalg.norm(emb - centroid) for emb in cluster_embeddings]
                key_idx = cluster_indices[np.argmin(distances)]
                key_points.append({
                    "text": sentences[key_idx],
                    "cluster_id": i,
                    "embedding": embeddings[key_idx].tolist()
                })
        logger.info(f"Extracted {len(key_points)} key points")
        return key_points