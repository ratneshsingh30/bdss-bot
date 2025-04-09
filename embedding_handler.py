import os
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingHandler:
    """
    Class to handle document embeddings and similarity search.
    """
    
    def __init__(self):
        """Initialize the embedding model and storage."""
        self.vectorizer = TfidfVectorizer()
        self.documents = []
        self.document_chunks = []
        self.metadatas = []
        self.vectors = None
        
    def add_document(self, text: str, metadata: Dict[str, Any], chunk_size: int = 1000) -> None:
        """
        Add a document to the embedding store.
        
        Args:
            text: The document text
            metadata: Metadata about the document
            chunk_size: Size to chunk the document
        """
        from document_processor import DocumentProcessor
        
        # Store the original document
        doc_id = len(self.documents)
        self.documents.append({
            "id": doc_id,
            "text": text,
            "metadata": metadata
        })
        
        # Chunk the document
        chunks = DocumentProcessor.chunk_text(text, chunk_size)
        
        if not chunks:
            return
            
        # Store chunk metadata
        for i, chunk in enumerate(chunks):
            self.document_chunks.append(chunk)
            self.metadatas.append({
                "document_id": doc_id,
                "chunk_id": i,
                "file_name": metadata["file_name"],
                "chunk_text": chunk[:100] + "..." if len(chunk) > 100 else chunk
            })
        
        # Recompute TF-IDF vectors for all chunks
        self.vectors = self.vectorizer.fit_transform(self.document_chunks)
    
    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for documents similar to the query.
        
        Args:
            query: The query text
            top_k: Number of top results to return
            
        Returns:
            List of documents with their similarity scores
        """
        if not self.document_chunks or self.vectors is None:
            return []
            
        # Transform query to TF-IDF vector
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.vectors).flatten()
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Format results
        results = []
        for idx in top_indices:
            metadata = self.metadatas[idx]
            document_id = metadata["document_id"]
            document = self.documents[document_id]
            
            results.append({
                "chunk": self.document_chunks[idx],
                "score": float(similarities[idx]),
                "metadata": metadata,
                "document_metadata": document["metadata"]
            })
            
        return results
    
    def get_context_for_query(self, query: str, top_k: int = 3) -> str:
        """
        Get relevant context for a query from stored documents.
        
        Args:
            query: The query text
            top_k: Number of chunks to include in context
            
        Returns:
            String with relevant context
        """
        results = self.similarity_search(query, top_k)
        
        if not results:
            return ""
            
        # Combine the chunks with source information
        context = ""
        for i, result in enumerate(results):
            context += f"\n\nContext {i+1} (from {result['metadata']['file_name']}):\n"
            context += result["chunk"]
            
        return context.strip()
