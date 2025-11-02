import os
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
from dotenv import load_dotenv

from document_processor import DocumentProcessor
from rag_engine import RAGEngine

load_dotenv()

app = FastAPI(title="DocInsight API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

doc_processor = DocumentProcessor()
rag_engine = None


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]


@app.get("/")
async def root():
    return {"message": "DocInsight API is running"}


@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process multiple documents"""
    global rag_engine
    
    try:
        uploaded_files = []
        all_documents = []
        
        for file in files:
            # Save file
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Process document
            documents = doc_processor.process_document(file_path)
            all_documents.extend(documents)
            uploaded_files.append(file.filename)
        
        # Initialize RAG engine with all documents
        rag_engine = RAGEngine()
        rag_engine.index_documents(all_documents)
        
        return {
            "message": f"Successfully uploaded and processed {len(uploaded_files)} file(s)",
            "files": uploaded_files,
            "chunks": len(all_documents)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the indexed documents"""
    global rag_engine
    
    if rag_engine is None:
        raise HTTPException(status_code=400, detail="No documents uploaded yet")
    
    try:
        answer, sources = rag_engine.query(request.question)
        return QueryResponse(answer=answer, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/clear")
async def clear_documents():
    """Clear all uploaded documents and reset the system"""
    global rag_engine
    
    try:
        for file in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        
        rag_engine = None
        
        return {"message": "All documents cleared"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "documents_indexed": rag_engine is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

