import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

class VectorDB:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the VectorDB with a sentence transformer model
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.faq_data = []
        self.embeddings = []
        
    def load_faq_data(self, faq_file_path):
        """
        Load FAQ data from JSON file
        """
        with open(faq_file_path, 'r', encoding='utf-8') as f:
            self.faq_data = json.load(f)
        
        # Create embeddings for all questions
        questions = [entry['question'] for entry in self.faq_data]
        self.embeddings = self.model.encode(questions)
        
        # Add embeddings to FAISS index
        self.index.add(np.array(self.embeddings).astype('float32'))
        
        print(f"Loaded {len(self.faq_data)} FAQ entries and created embeddings")
        
    def search(self, query, k=3):
        """
        Search for the most similar FAQ entries to the query
        Returns the top k most similar entries
        """
        # Encode the query
        query_embedding = self.model.encode([query])
        
        # Search in the FAISS index
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        
        # Return the most similar FAQ entries
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.faq_data):  # Check bounds
                results.append({
                    'question': self.faq_data[idx]['question'],
                    'answer': self.faq_data[idx]['answer'],
                    'source': self.faq_data[idx]['source'],
                    'distance': float(distances[0][i])
                })
        
        return results

# Initialize global vector database
vector_db = None

def initialize_vector_db():
    """
    Initialize the global vector database
    """
    global vector_db
    if vector_db is None:
        vector_db = VectorDB()
        faq_file_path = 'mf_faq_data.json'
        if os.path.exists(faq_file_path):
            vector_db.load_faq_data(faq_file_path)
        else:
            print(f"FAQ file {faq_file_path} not found")
    return vector_db

def search_similar_questions(query, k=3):
    """
    Search for similar questions in the vector database
    """
    db = initialize_vector_db()
    return db.search(query, k)