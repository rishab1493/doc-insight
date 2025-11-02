import sys

_base_requirements = [
    'fastapi',
    'uvicorn',
    'python-multipart',
    'python-dotenv',
    'sentence-transformers',
    'faiss-cpu',
    'PyPDF2',
    'openpyxl',
    'python-docx',
    'pandas',
    'transformers',
    'torch',
]

sdk: gradio
sdk_version: 4.7.1
app_file: app.py
pinned: false

