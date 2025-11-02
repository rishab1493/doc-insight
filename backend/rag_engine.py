import os
from typing import List, Tuple, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()


class RAGEngine:
    """RAG engine using HuggingFace models and FAISS"""
    
    def __init__(self):
        # Initialize embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
        
        # Initialize QA model with smaller, more efficient model
        print("Loading QA model...")
        try:
            self.qa_pipeline = pipeline(
                "text2text-generation",
                model="google/flan-t5-base",
                max_length=512
            )
        except Exception as e:
            print(f"Error loading model: {e}")
            self.qa_pipeline = None
        
        # Initialize FAISS index
        self.index = None
        self.documents = []
        self.document_embeddings = []
    
    def index_documents(self, documents: List[Dict[str, str]]):
        """Index documents using FAISS"""
        print(f"Indexing {len(documents)} documents...")
        
        self.documents = documents
        contents = [doc['content'] for doc in documents]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(contents, show_progress_bar=True)
        self.document_embeddings = embeddings
        
        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(np.array(embeddings).astype('float32'))
        
        print(f"Successfully indexed {len(documents)} documents")
    
    def query(self, question: str, top_k: int = 3) -> Tuple[str, List[str]]:
        """
        Query the indexed documents
        Returns: (answer, list of source references)
        """
        if self.index is None or len(self.documents) == 0:
            raise ValueError("No documents indexed")
        
        # Encode question
        question_embedding = self.embedding_model.encode([question])
        
        # Search FAISS index
        distances, indices = self.index.search(
            np.array(question_embedding).astype('float32'), 
            top_k
        )
        
        # Get relevant documents
        relevant_docs = [self.documents[i] for i in indices[0]]
        context = "\n\n".join([doc['content'] for doc in relevant_docs])
        sources = [doc['source'] for doc in relevant_docs]
        
        # Generate answer using context
        answer = self._generate_answer(question, context)
        
        return answer, sources
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using HuggingFace model"""
        
        prompt = f"""Answer the question based on the context below.

Context: {context[:1500]}

Question: {question}

Answer:"""
        
        if self.qa_pipeline is None:
            return self._extractive_answer(question, context)
        
        try:
            result = self.qa_pipeline(
                prompt,
                max_length=200,
                do_sample=False
            )
            answer = result[0]['generated_text'].strip()
            
        except Exception as e:
            print(f"Generation error: {e}, using extractive fallback")
            answer = self._extractive_answer(question, context)
        
        return answer
    
    def _extractive_answer(self, question: str, context: str) -> str:
        """Simple extractive answer as fallback"""
        # Return first relevant paragraph
        paragraphs = context.split('\n\n')
        if paragraphs:
            return paragraphs[0][:500] + "..."
        return "Unable to generate answer from the provided documents."

