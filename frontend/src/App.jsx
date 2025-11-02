import { useState } from 'react';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import { uploadDocuments, queryDocuments, clearDocuments } from './utils/api';
import './index.css';

function App() {
  const [isUploading, setIsUploading] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);
  const [hasDocuments, setHasDocuments] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleUpload = async (files) => {
    setIsUploading(true);
    setUploadStatus(null);

    try {
      const response = await uploadDocuments(files);
      setUploadStatus({
        type: 'success',
        message: `Successfully uploaded ${response.files.length} file(s) with ${response.chunks} chunks`,
      });
      setHasDocuments(true);
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || 'Failed to upload documents',
      });
    } finally {
      setIsUploading(false);
    }
  };

  const handleQuery = async (question) => {
    setIsQuerying(true);
    try {
      const response = await queryDocuments(question);
      return response;
    } finally {
      setIsQuerying(false);
    }
  };

  const handleClear = async () => {
    if (window.confirm('Are you sure you want to clear all documents?')) {
      try {
        await clearDocuments();
        setHasDocuments(false);
        setUploadStatus({
          type: 'success',
          message: 'All documents cleared',
        });
      } catch (error) {
        setUploadStatus({
          type: 'error',
          message: 'Failed to clear documents',
        });
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">DocInsight</h1>
          <p className="text-gray-600">
            Smart Document Chat Interface powered by RAG
          </p>
        </header>

        {uploadStatus && (
          <div
            className={`max-w-2xl mx-auto mb-6 p-4 rounded-lg ${
              uploadStatus.type === 'success'
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }`}
          >
            <p>{uploadStatus.message}</p>
          </div>
        )}

        <div className="mb-8">
          <FileUpload onUpload={handleUpload} isLoading={isUploading} />
        </div>

        {hasDocuments && (
          <div className="text-center mb-4">
            <button
              onClick={handleClear}
              className="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition-colors"
            >
              Clear All Documents
            </button>
          </div>
        )}

        <div className="mb-8">
          <ChatInterface
            onQuery={handleQuery}
            isLoading={isQuerying}
            hasDocuments={hasDocuments}
          />
        </div>

        <footer className="text-center text-gray-600 text-sm mt-12">
          <p>Built with React, FastAPI, and HuggingFace Transformers</p>
        </footer>
      </div>
    </div>
  );
}

export default App;

