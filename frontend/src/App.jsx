// frontend/src/App.jsx
import React, { useState } from 'react';

function App() {
  const [userQuery, setUserQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');

  const handleQueryChange = (event) => {
    setUserQuery(event.target.value);
  };

  const handleSubmitQuery = () => {
    setAiResponse("AI is thinking... (This is a placeholder response)");
    console.log("Processing query:", userQuery);
  };

  return (
    <div className="flex flex-col items-center pt-30 min-h-screen bg-gray-100">
      <h1 className="text-3xl font-bold underline">Venture Assist AI</h1>
        <p className="text-lg text-gray-600 mt-4 max-w-md text-center">
          Your AI partner for all venture needs: from idea to pitch, marketing to meetings.
        </p>

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
        >
          Get AI Assistance
        </button>
      </div>

      {aiResponse && (
        <div className="max-w-xl mx-auto mt-6 p-6 bg-white rounded-2xl shadow-lg">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">AI Response</h2>
          <p className="text-gray-700 whitespace-pre-wrap">
            {aiResponse}
          </p>
        </div>
      )}
    </div>
  )
}

export default App
