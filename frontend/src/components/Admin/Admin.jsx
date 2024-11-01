import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DocumentPanel from '../DocumentPanel/DocumentPanel.jsx';

const Admin = () => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setUploadStatus('');
    } else {
      setFile(null);
      setUploadStatus('Please select a PDF file');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log('Uploading file:', file.name);

      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/upload`, {
        method: 'POST',
        headers: {
          'Authorization': token
        },
        body: formData
      });

      console.log('Response status:', response.status);

      if (response.ok) {
        setUploadStatus('File uploaded successfully');
        setFile(null);
      } else {
        const data = await response.json();
        console.error('Upload error:', data);
        setUploadStatus(
          `Upload failed: ${data.message || 'Unknown error'} (Status: ${response.status})`
        );
      }
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus(`Error uploading file: ${error.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="w-screen h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <div className="w-full bg-white shadow-sm p-4 flex justify-between items-center">
        <h1 className="text-xl font-semibold">Admin Dashboard</h1>
        <div className="flex gap-4">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
          >
            Chat Dashboard
          </button>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm text-red-600 hover:text-red-800"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6 overflow-auto">
        <div className="max-w-4xl mx-auto">
          {/* Document Status Panels */}
          <DocumentPanel />

          {/* Upload Section */}
          <div className="mt-6 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold mb-4">Upload PDF</h2>
            <form onSubmit={handleUpload} className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="w-full"
                  disabled={isUploading}
                />
                {file && (
                  <p className="mt-2 text-sm text-gray-600">
                    Selected file: {file.name}
                  </p>
                )}
              </div>

              <button
                type="submit"
                disabled={!file || isUploading}
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isUploading ? 'Uploading...' : 'Upload PDF'}
              </button>

              {uploadStatus && (
                <p className={`text-sm ${
                  uploadStatus.includes('successfully') 
                    ? 'text-green-600' 
                    : 'text-red-600'
                }`}>
                  {uploadStatus}
                </p>
              )}
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Admin;