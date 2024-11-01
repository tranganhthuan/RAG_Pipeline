import React, { useState, useEffect } from 'react';


const DocumentPanels = () => {
  const [uploadedDocs, setUploadedDocs] = useState([]);
  const [processedDocs, setProcessedDocs] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  const fetchDocuments = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      const headers = { 'Authorization': token };

      // Fetch both sets of documents
      const [uploadedResponse, processedResponse] = await Promise.all([
        fetch(`${import.meta.env.VITE_BACKEND_URL}/api/get_uploaded_documents`, { headers }),
        fetch(`${import.meta.env.VITE_BACKEND_URL}/api/get_rag_documents`, { headers })
      ]);

      if (!uploadedResponse.ok || !processedResponse.ok) {
        throw new Error('Failed to fetch documents');
      }

      const uploadedData = await uploadedResponse.json();
      const processedData = await processedResponse.json();

      // Filter out processed documents from uploaded documents to get pending ones
      const pendingDocs = uploadedData.documents.filter(
        doc => !processedData.documents.includes(doc)
      );

      setUploadedDocs(pendingDocs);
      setProcessedDocs(processedData.documents);
      setError('');
    } catch (err) {
      setError('Error fetching documents: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const DocumentList = ({ documents, emptyMessage, onDelete }) => (
    <div className="space-y-2">
      {documents.length === 0 ? (
        <p className="text-gray-500 italic">{emptyMessage}</p>
      ) : (
        documents.map((doc, index) => (
          <div
            key={index}
            className="p-3 bg-white rounded-md shadow-sm hover:shadow-md transition-shadow flex justify-between items-center"
          >
            <span>{doc}</span>
            {onDelete && (
              <button
                onClick={() => onDelete(doc)}
                className="p-2 text-red-600 hover:text-red-800"
              >
                Delete
              </button>
            )}
          </div>
        ))
      )}
    </div>
  );

  const RefreshButton = () => (
    <button
      onClick={fetchDocuments}
      disabled={isLoading}
      className="px-4 py-2 text-sm text-blue-600 hover:text-blue-800 bg-white rounded-md border border-blue-300 hover:border-blue-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {isLoading ? 'Refreshing...' : 'Refresh Documents'}
    </button>
  );

  const deleteDocument = async (doc) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/delete_document/${doc}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token
        },
      });

      if (!response.ok) {
        throw new Error('Failed to delete document');
      }

      // Refresh documents after successful deletion
      fetchDocuments();
    } catch (err) {
      setError('Error deleting document: ' + err.message);
    }
  };

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-600">{error}</p>
        <button
          onClick={fetchDocuments}
          className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Refresh Button */}
      <div className="flex justify-end">
        <RefreshButton />
      </div>

      {/* Pending Documents Panel */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Pending Documents</h2>
          <span className="bg-yellow-100 text-yellow-800 text-sm py-1 px-3 rounded-full">
            {uploadedDocs.length} pending
          </span>
        </div>
        {isLoading ? (
          <div className="flex justify-center py-4">
            <div className="animate-pulse text-gray-400">Loading...</div>
          </div>
        ) : (
          <DocumentList
            documents={uploadedDocs}
            emptyMessage="No pending documents"
          />
        )}
      </div>

      {/* Processed Documents Panel */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Processed Documents</h2>
          <span className="bg-green-100 text-green-800 text-sm py-1 px-3 rounded-full">
            {processedDocs.length} completed
          </span>
        </div>
        {isLoading ? (
          <div className="flex justify-center py-4">
            <div className="animate-pulse text-gray-400">Loading...</div>
          </div>
        ) : (
          <DocumentList
            documents={processedDocs}
            emptyMessage="No processed documents"
            onDelete={(doc) => {
              deleteDocument(doc);
            }}
          />
        )}
      </div>
    </div>
  );
};

export default DocumentPanels;