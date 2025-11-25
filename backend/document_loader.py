"""
Document loader for PDFs and company information.
"""
import os
import json
from typing import List, Dict
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from sqlalchemy.orm import Session
from database import Document
from config import get_settings
import requests
from bs4 import BeautifulSoup

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)


class DocumentLoader:
    """Load and process documents for the RAG system."""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
        )
    
    def load_pdf(self, pdf_path: str) -> List[str]:
        """Load and extract text from PDF."""
        print(f"Loading PDF: {pdf_path}")
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        return self.text_splitter.split_text(text)
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding vector for text using OpenAI."""
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def load_company_info(self) -> str:
        """Load company information."""
        company_info = """
        Company Name: Spapperi N.T. S.r.l.
        
        About:
        Spapperi N.T. S.r.l. was founded in the early 1960s and operates with excellent market results 
        in several international countries. The company headquarters, recently inaugurated, covers 
        approximately 4,000 m² and is located in Z.A. fraz. San Secondo 06012 in Città di Castello, PG, Italy.
        
        Specialization:
        Spapperi specializes in agricultural machinery with a focus on Italian-made innovation. 
        The company produces a wide range of equipment including:
        - Tobacco line machinery
        - Transplanters (TN 100, TP series)
        - Pneumatic seeders (SMP)
        - Film layers (SF)
        - Ridge formers (SM)
        - Harvesting equipment
        - Machinery for medicinal herbs and lavender
        
        Contact Information:
        Address: Via Pietro Ercolani, 5 b, 06012 Città di Castello PG, ITALY
        Phone: +39 075 85 78 156
        Fax: +39 075 85 78 848
        Email: info@spapperi.com
        Website: https://www.spapperi.com/it/
        VAT: P. IVA 03467460543
        
        Key Products:
        - RA832: Tobacco harvester
        - MI100/MI100S: Semi-automatic harvester for medicinal herbs
        - SMP: Pneumatic seeder
        - BR 712: Trailer with vegetable collection belt
        - SFB: Combined bed former
        - TN 100: Transplanter
        
        Innovation:
        Spapperi represents Italian-made innovation in agricultural machinery, 
        combining traditional craftsmanship with modern technology.
        """
        return company_info
    
    def store_documents(self, db: Session, texts: List[str], source: str):
        """Store document chunks in the database with embeddings."""
        print(f"Storing {len(texts)} chunks from {source}")
        
        for i, text in enumerate(texts):
            print(f"Processing chunk {i+1}/{len(texts)}")
            embedding = self.get_embedding(text)
            
            doc = Document(
                content=text,
                source=source,
                doc_metadata=json.dumps({"chunk_index": i}),
                embedding=embedding
            )
            db.add(doc)
        
        db.commit()
        print(f"Successfully stored documents from {source}")
    
    def load_all_documents(self, db: Session):
        """Load all PDFs and company information into the database."""
        # Check if documents already exist
        existing_docs = db.query(Document).first()
        if existing_docs:
            print("Documents already loaded in database. Skipping...")
            return
        
        # Load company information
        print("Loading company information...")
        company_text = self.load_company_info()
        company_chunks = self.chunk_text(company_text)
        self.store_documents(db, company_chunks, "company_info")
        
        # Load PDFs
        pdf_dir = "/data"
        pdf_files = [
            "Piantatalee-TP.pdf",
            "Rincalzatore-SM.pdf",
            "Seminatrice-pneumatica-SMP.pdf",
            "Stendi-film-SF.pdf"
        ]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            if os.path.exists(pdf_path):
                print(f"\nProcessing {pdf_file}...")
                text = self.load_pdf(pdf_path)
                chunks = self.chunk_text(text)
                self.store_documents(db, chunks, pdf_file)
            else:
                print(f"Warning: {pdf_path} not found")
        
        print("\n✓ All documents loaded successfully!")


