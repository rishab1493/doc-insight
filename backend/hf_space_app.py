# For HuggingFace Spaces Deployment
# Copy this file as a template for deploying to HuggingFace Spaces

import os
import gradio as gr
from main import app
import uvicorn
from threading import Thread

# Start FastAPI server in background
def start_server():
    uvicorn.run(app, host="0.0.0.0", port=7860)

# Create a simple Gradio interface as a placeholder
# The actual API will be accessible via the FastAPI endpoints
demo = gr.Interface(
    fn=lambda: "DocInsight API is running. Use the API endpoints to interact with the service.",
    inputs=None,
    outputs="text",
    title="DocInsight API",
    description="Upload documents and query them using the REST API endpoints."
)

if __name__ == "__main__":
    # Start FastAPI in background thread
    thread = Thread(target=start_server, daemon=True)
    thread.start()
    
    # Launch Gradio interface
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

