from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
import re
import logging

logger = logging.getLogger(__name__)

class KeyPointExtractionAgent:
    def __init__(self):
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("SentenceTransformer model loaded")

    def preprocess_text(self, text):
        # Split on common section markers
        sections = re.split(r'\d+\.|•|\n\n|\r\n\r\n', text)
        # Clean up sections
        sections = [s.strip() for s in sections if s.strip()]
        # Further split long sections into sentences
        sentences = []
        for section in sections:
            # Split on period followed by space or newline
            section_sentences = re.split(r'(?<=[.!?])\s+', section)
            sentences.extend([s.strip() for s in section_sentences if s.strip()])
        return sentences

    def extract_key_points(self, transcription):
        logger.info("Extracting key points from transcription")
        
        # Preprocess text into meaningful chunks
        sentences = self.preprocess_text(transcription)
        
        if len(sentences) < 2:
            logger.info("Transcription too short, returning single key point")
            return [{"text": transcription, "cluster_id": 0, "embedding": self.sentence_model.encode([transcription])[0].tolist()}]
        
        # Generate embeddings for all sentences
        embeddings = self.sentence_model.encode(sentences)
        
        # Determine number of clusters based on content length
        num_clusters = min(max(3, len(sentences) // 3), 15)  # At least 3, at most 15 clusters
        
        # Cluster similar sentences
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(embeddings)
        
        # Extract key points from each cluster
        key_points = []
        for i in range(num_clusters):
            cluster_indices = [j for j, label in enumerate(kmeans.labels_) if label == i]
            if cluster_indices:
                # Get all sentences in this cluster
                cluster_sentences = [sentences[idx] for idx in cluster_indices]
                cluster_embeddings = embeddings[cluster_indices]
                
                # Find the most representative sentence (closest to centroid)
                centroid = kmeans.cluster_centers_[i]
                distances = [np.linalg.norm(emb - centroid) for emb in cluster_embeddings]
                key_idx = cluster_indices[np.argmin(distances)]
                
                # Clean up the key point text
                key_point_text = sentences[key_idx].strip()
                # Remove redundant markers
                key_point_text = re.sub(r'^[-•●\s]+', '', key_point_text)
                
                if len(key_point_text) > 10:  # Only add if the key point is meaningful
                    key_points.append({
                        "text": key_point_text,
                        "cluster_id": i,
                        "embedding": embeddings[key_idx].tolist(),
                        "similar_points": [s for s in cluster_sentences if s != key_point_text][:3]  # Store up to 3 similar points
                    })
        
        # Sort key points by their position in the original text
        key_points.sort(key=lambda x: transcription.find(x["text"]))
        
        logger.info(f"Extracted {len(key_points)} key points")
        return key_points