// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function App() {
  const [userQuery, setUserQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [authStatus, setAuthStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const VITE_REACT_APP_BACKEND_URL = import.meta.env.VITE_REACT_APP_BACKEND_URL;
  const GOOGLE_AUTH_URL = `${VITE_REACT_APP_BACKEND_URL}/auth/google`;
  
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const status = params.get('auth_status');
    const error = params.get('error');

    if (status === 'success') {
      setAuthStatus('Google Connected Successfully! You can now use AI features.');
      
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (status === 'failed') {
      setAuthStatus(`Google Connection Failed: ${error || 'Unknown error'}. Please try again.`);
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const handleQueryChange = (event) => {
    setUserQuery(event.target.value);
  };

  const handleSubmitQuery = async () => {
    if (!userQuery.trim()) return;

    setIsLoading(true);
    setAiResponse("");

    try {
      const response = await fetch(VITE_REACT_APP_BACKEND_URL + '/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userQuery }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAiResponse(data.response);
      setUserQuery('');
    } catch (error) {
      console.error("Error sending query to backend:", error);
      setAiResponse("Error: Could not get response from AI. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleConnectGoogle = () => {
    window.location.href = GOOGLE_AUTH_URL;
  };

  return (
    <div className="flex flex-col items-center pt-30 min-h-screen bg-gray-100">
      <h1 className="text-3xl font-bold underline">Venture Assist AI</h1>
      <p className="text-lg text-gray-600 mt-4 max-w-md text-center">
        Your AI partner for all venture needs: from idea to pitch, marketing to meetings.
      </p>

      {authStatus && (
        <div className={`mt-4 p-3 rounded-lg text-center ${authStatus.includes('Failed') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
          {authStatus}
        </div>
      )}

      <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-2xl shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">How can I help you today?</h2>
        <textarea 
          rows="5" 
          placeholder="For example: Summarize my business idea. Create a logo for a sustainable fashion brand. Research market trends for AI in healthcare. Schedule a meeting with investors. Generate a pitch deck draft."
          className="w-full p-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none text-gray-800"
          value={userQuery}
          onChange={handleQueryChange}
        ></textarea>
        <button
          className="mt-4 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-6 rounded-xl transition-all"
          onClick={handleSubmitQuery}
          disabled={isLoading}
        >
          {isLoading ? 'Thinking...' : 'Get AI Assistance'}
        </button>

        <button
          className="mt-4 w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-xl transition-all"
          onClick={handleConnectGoogle}
        >
          Connect Google
        </button>
      </div>

      {(aiResponse || isLoading) && (
        <div className="max-w-xl mx-auto mt-6 p-6 bg-white rounded-2xl shadow-lg">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">AI Response</h2>
          {isLoading && !aiResponse && <p className="text-gray-700 text-center">AI is thinking...</p>}
            {aiResponse && (
              <div className="prose max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {aiResponse}
                </ReactMarkdown>
              </div>
            )}
        </div>
      )}
    </div>
  )
}

export default App
