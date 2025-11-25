"""
RAG Agent for querying Spapperi documents.
"""
from typing import List, Dict
from sqlalchemy.orm import Session
from openai import OpenAI
from database import Document
from config import get_settings
import numpy as np

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)


class RAGAgent:
    """Retrieval-Augmented Generation Agent."""
    
    def __init__(self):
        self.system_prompt = """You are an expert assistant for Spapperi N.T. S.r.l., 
an Italian agricultural machinery company. You have deep knowledge about their products, 
services, and company information.

Your role is to:
- Provide accurate information about Spapperi's agricultural machinery
- Answer technical questions about their products
- Help customers understand product specifications and features
- Provide contact information when needed
- Be professional, helpful, and knowledgeable

Always base your answers on the provided context. If you don't know something based 
on the context, say so honestly. You can respond in multiple languages based on 
the customer's question.

Context information:
{context}
"""
    
    def get_query_embedding(self, query: str) -> List[float]:
        """Get embedding for the query."""
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=query
        )
        return response.data[0].embedding
    
    def search_similar_documents(self, db: Session, query_embedding: List[float], 
                                top_k: int = None) -> List[Dict]:
        """Search for similar documents using vector similarity."""
        if top_k is None:
            top_k = settings.top_k_results
        
        # Use pgvector's <=> operator for cosine distance
        results = db.query(
            Document.content,
            Document.source,
            Document.embedding.cosine_distance(query_embedding).label('distance')
        ).order_by('distance').limit(top_k).all()
        
        return [
            {
                "content": result.content,
                "source": result.source,
                "distance": result.distance
            }
            for result in results
        ]
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """Generate response using OpenAI with retrieved context."""
        # Build context from retrieved documents
        context = "\n\n".join([
            f"[Source: {doc['source']}]\n{doc['content']}"
            for doc in context_docs
        ])
        
        # Create messages for OpenAI
        messages = [
            {
                "role": "system",
                "content": self.system_prompt.format(context=context)
            },
            {
                "role": "user",
                "content": query
            }
        ]
        
        # Generate response
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    def query(self, db: Session, question: str) -> Dict:
        """
        Process a query through the RAG pipeline.
        
        Args:
            db: Database session
            question: User's question
            
        Returns:
            Dict containing answer, sources, and metadata
        """
        # Get query embedding
        query_embedding = self.get_query_embedding(question)
        
        # Retrieve similar documents
        similar_docs = self.search_similar_documents(db, query_embedding)
        
        # Generate response
        answer = self.generate_response(question, similar_docs)
        
        # Prepare response
        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "source": doc["source"],
                    "relevance_score": 1 - doc["distance"]  # Convert distance to similarity
                }
                for doc in similar_docs
            ],
            "context_used": len(similar_docs)
        }


