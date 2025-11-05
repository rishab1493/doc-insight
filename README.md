# DocInsight

A Smart Document Chat Interface for interacting with your documents using AI-powered Retrieval-Augmented Generation (RAG). Built specifically for analyzing account statements, financial documents, PDFs, and Excel sheets.

## Features

- Upload and parse multiple document formats (PDF, Excel, CSV, TXT)
- AI-powered chat interface to query your documents
- RAG-based retrieval for accurate, context-aware responses
- Secure document processing with local embeddings
- Modern, responsive UI built with React
- Fast Python backend with FastAPI

## Architecture

- **Frontend**: React + Vite + TailwindCSS
- **Backend**: Python FastAPI + LangChain + HuggingFace
- **Vector Store**: FAISS (in-memory)
- **Embeddings**: HuggingFace sentence-transformers
- **LLM**: HuggingFace Inference API

## Use Cases

- Query your bank account statements
- Extract information from financial documents
- Analyze spending patterns across multiple documents
- Search through uploaded PDFs and Excel sheets
- Get instant answers without manual document review

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- HuggingFace API token (free tier available)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Deployment

### Frontend (Vercel/Netlify)

The frontend can be deployed for free on Vercel or Netlify:

**Vercel:**

```bash
cd frontend
vercel deploy
```

**Netlify:**

```bash
cd frontend
npm run build
# Deploy the dist/ folder
```

### Backend (Free Options)

1. **HuggingFace Spaces** (Recommended)

   - Free GPU support
   - Built for ML applications
   - Push to HF Spaces repository

2. **Railway**

   - 500 hours/month free tier
   - Easy GitHub integration

3. **Render**

   - Free tier available
   - Sleeps after 15 min inactivity

4. **Modal**
   - Serverless Python
   - Pay-per-use pricing

## Environment Variables

### Backend

- `UPLOAD_DIR`: Directory for temporary file storage (default: ./uploads)
- `MAX_FILE_SIZE`: Maximum upload size in MB (default: 10)

### Frontend

- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

## Security Notes

- Documents are processed temporarily and not permanently stored
- Embeddings are stored in memory during session
- Use environment variables for sensitive tokens
- For production, implement proper authentication

## Tech Stack

- **Frontend**: React, Vite, TailwindCSS, Axios
- **Backend**: FastAPI, LangChain, HuggingFace Transformers
- **Document Processing**: PyPDF2, openpyxl, python-docx
- **Vector Store**: FAISS
- **Embeddings**: sentence-transformers

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
