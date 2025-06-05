// frontend/src/App.jsx

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 class="text-3xl font-bold underline">Venture Assist AI</h1>
        <p class="text-lg text-gray-600 mt-4 max-w-md text-center">
          Turn your startup idea into an investor-ready pitch - with AI.
        </p>

      <div class="max-w-xl mx-auto mt-10 p-6 bg-white rounded-2xl shadow-lg">
        <h2 class="text-2xl font-bold text-gray-800 mb-4 text-center">Describe your startup idea</h2>
        <textarea 
          rows="5" 
          placeholder="For example: Selling homes with AI."
          class="w-full p-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none text-gray-800"
        ></textarea>
        <button 
          class="mt-4 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-6 rounded-xl transition-all"
        >
          Validate Idea
        </button>
      </div>
    </div>
  )
}

export default App
