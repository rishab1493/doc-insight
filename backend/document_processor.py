import os
from typing import List, Dict
from PyPDF2 import PdfReader
import openpyxl
import docx
import pandas as pd


class DocumentProcessor:
    """Process various document types and extract text"""
    
    def __init__(self):
        self.supported_extensions = ['.pdf', '.xlsx', '.xls', '.docx', '.txt', '.csv']
    
    def process_document(self, file_path: str) -> List[Dict[str, str]]:
        """
        Process a document and return chunks with metadata
        Returns: List of dicts with 'content' and 'source' keys
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self._process_pdf(file_path)
        elif ext in ['.xlsx', '.xls']:
            return self._process_excel(file_path)
        elif ext == '.docx':
            return self._process_docx(file_path)
        elif ext == '.txt':
            return self._process_txt(file_path)
        elif ext == '.csv':
            return self._process_csv(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _process_pdf(self, file_path: str) -> List[Dict[str, str]]:
        """Extract text from PDF"""
        documents = []
        reader = PdfReader(file_path)
        
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                # Split into chunks if text is too long
                chunks = self._chunk_text(text, chunk_size=1000)
                for i, chunk in enumerate(chunks):
                    documents.append({
                        'content': chunk,
                        'source': f"{os.path.basename(file_path)} (Page {page_num}, Chunk {i+1})"
                    })
        
        return documents
    
    def _process_excel(self, file_path: str) -> List[Dict[str, str]]:
        """Extract text from Excel"""
        documents = []
        
        try:
            # Read all sheets
            df_dict = pd.read_excel(file_path, sheet_name=None)
            
            for sheet_name, df in df_dict.items():
                # Convert dataframe to string representation
                text = df.to_string()
                if text.strip():
                    chunks = self._chunk_text(text, chunk_size=1000)
                    for i, chunk in enumerate(chunks):
                        documents.append({
                            'content': chunk,
                            'source': f"{os.path.basename(file_path)} (Sheet: {sheet_name}, Chunk {i+1})"
                        })
        
        except Exception as e:
            raise ValueError(f"Error processing Excel file: {str(e)}")
        
        return documents
    
    def _process_docx(self, file_path: str) -> List[Dict[str, str]]:
        """Extract text from Word document"""
        documents = []
        doc = docx.Document(file_path)
        
        text = "\n".join([para.text for para in doc.paragraphs])
        if text.strip():
            chunks = self._chunk_text(text, chunk_size=1000)
            for i, chunk in enumerate(chunks):
                documents.append({
                    'content': chunk,
                    'source': f"{os.path.basename(file_path)} (Chunk {i+1})"
                })
        
        return documents
    
    def _process_txt(self, file_path: str) -> List[Dict[str, str]]:
        """Extract text from TXT file"""
        documents = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if text.strip():
            chunks = self._chunk_text(text, chunk_size=1000)
            for i, chunk in enumerate(chunks):
                documents.append({
                    'content': chunk,
                    'source': f"{os.path.basename(file_path)} (Chunk {i+1})"
                })
        
        return documents
    
    def _process_csv(self, file_path: str) -> List[Dict[str, str]]:
        """Extract text from CSV file"""
        documents = []
        
        try:
            df = pd.read_csv(file_path)
            text = df.to_string()
            
            if text.strip():
                chunks = self._chunk_text(text, chunk_size=1000)
                for i, chunk in enumerate(chunks):
                    documents.append({
                        'content': chunk,
                        'source': f"{os.path.basename(file_path)} (Chunk {i+1})"
                    })
        
        except Exception as e:
            raise ValueError(f"Error processing CSV file: {str(e)}")
        
        return documents
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.5:  # Only break if we're past halfway
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if c]

