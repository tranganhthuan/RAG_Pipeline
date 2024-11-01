import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/20/solid'

const Dashboard = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();
  const [selectedModel, setSelectedModel] = useState('Gemini');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Check if token exists
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    // Add user message to chat
    setMessages(prev => [...prev, { text: inputText, sender: 'user' }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token
        },
        body: JSON.stringify({ text: inputText, model: selectedModel.toLowerCase() })
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(prev => [...prev, { 
          text: data.answer, 
          sender: 'bot',
          keywordMetadata: data.keyword_metadata,
          keywordContext: data.keyword_context,
          semanticMetadata: data.semantic_metadata, 
          semanticContext: data.semantic_context
        }]);
      } else if (response.status === 401) {
        // Token expired or invalid
        localStorage.removeItem('token');
        navigate('/login');
      } else {
        throw new Error('Failed to get response');
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        text: 'Sorry, I encountered an error processing your request.',
        sender: 'bot',
        isError: true
      }]);
    } finally {
      setIsLoading(false);
      setInputText('');
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
        <h1 className="text-xl font-semibold">RAG Chat Dashboard</h1>
        <div>
          <button
            onClick={() => navigate('/update')}
            className="px-4 py-2 text-sm text-blue-600 hover:text-blue-800"
          >
            Update
          </button>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm text-red-600 hover:text-red-800"
          >
            Logout
          </button>
          </div>
      </div>

      {/* Chat Container */}
      <div className="flex-1 overflow-hidden p-4 flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto mb-4">
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex flex-col gap-1 ${message.sender === 'user' ? 'max-w-4xl' : 'max-w-4xl'}`}>
                  <div
                    className={`w-full rounded-lg p-3 ${
                      message.sender === 'user'
                        ? 'bg-blue-500 text-white'
                        : message.isError
                        ? 'bg-red-100 text-red-700'
                        : 'bg-white text-gray-800'
                    } shadow`}
                  >
                    {message.text}
                  </div>

                  {message.sender === 'bot' && !message.isError && (
                    <div className="flex gap-2 text-xs text-gray-500">
                      {message.keywordMetadata && (
                        <div className="group relative">
                          <span
                            className="cursor-pointer underline decoration-dotted"
                            onClick={() => setMessages(prev => [...prev, {
                              text: message.keywordContext,
                              sender: 'bot'
                            }])}
                          >
                            {"Keyword metadata: " + message.keywordMetadata}
                          </span>
                          <div className="invisible group-hover:visible absolute bottom-full left-0 mb-2 w-64 rounded bg-gray-800 p-2 text-white text-xs">
                            {message.keywordContext}
                          </div>
                        </div>
                      )}
                      {message.semanticMetadata && (
                        <div className="group relative">
                          <span
                            className="cursor-pointer underline decoration-dotted"
                            onClick={() => setMessages(prev => [...prev, {
                              text: message.semanticContext,
                              sender: 'bot'
                            }])}
                          >
                            {"Semantic metadata: " + message.semanticMetadata}
                          </span>
                          <div className="invisible group-hover:visible absolute bottom-full left-0 mb-2 w-64 rounded bg-gray-800 p-2 text-white text-xs">
                            {message.semanticContext}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="max-w-4xl w-full rounded-lg p-3 bg-gray-100 text-gray-500">
                  Thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="w-full p-4 bg-white border-t">
          <form onSubmit={handleSubmit} className="flex flex-col gap-2">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Ask anything..."
                className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputText.trim()}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Send
              </button>
            </div>
            <Menu as="div" className="relative inline-block text-left">
              <div>
                <MenuButton className="inline-flex w-32 justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                  {selectedModel}
                  <ChevronDownIcon aria-hidden="true" className="-mr-1 size-5 text-gray-400" />
                </MenuButton>
              </div>

              <MenuItems className="absolute bottom-full left-0 z-10 mb-2 w-32 origin-bottom-right rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none">
                <div className="py-1">
                  <MenuItem>
                    <button
                      onClick={() => setSelectedModel('Gemini')}
                      className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                    >
                      Gemini
                    </button>
                  </MenuItem>
                  <MenuItem>
                    <button
                      onClick={() => setSelectedModel('OpenAI')}
                      className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                    >
                      OpenAI
                    </button>
                  </MenuItem>
                  <MenuItem>
                    <button
                      onClick={() => setSelectedModel('Ollama')}
                      className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                    >
                      Ollama
                    </button>
                  </MenuItem>
                </div>
              </MenuItems>
            </Menu>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;