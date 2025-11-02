# Deployment Guide

## HuggingFace Spaces Deployment

To deploy the backend on HuggingFace Spaces:

1. Create a new Space on huggingface.co
2. Choose "Gradio" as the SDK
3. Upload all backend files including:
   - main.py
   - document_processor.py
   - rag_engine.py
   - hf_space_app.py
   - requirements.txt
   - README_HF.md (rename to README.md in the Space)
4. Add a file named `README.md` in your Space with the content from README_HF.md
5. The Space will automatically build and deploy

Your API will be available at: `https://your-username-your-space-name.hf.space/`

## Railway Deployment

1. Create account on railway.app
2. Create new project from GitHub
3. Add environment variables:
   - `HUGGINGFACE_API_TOKEN`
   - `UPLOAD_DIR=/tmp/uploads`
4. Railway will auto-detect and deploy

## Render Deployment

1. Create account on render.com
2. Create new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables

## Modal Deployment

1. Install modal: `pip install modal`
2. Authenticate: `modal token new`
3. Deploy: `modal deploy backend_modal.py`

Backend will be available at the provided URL.

