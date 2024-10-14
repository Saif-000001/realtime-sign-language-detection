import React, { useState, useRef, useEffect } from 'react';
import LiveDetection from './components/LiveDetection';
import ImageUpload from './components/ImageUpload';

function App() {
  const [activeTab, setActiveTab] = useState('live');

  return (
    <div className="bg-gray-100 min-h-screen flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-2xl">
        <h1 className="text-3xl font-bold mb-6 text-center">Realtime Sign Language Detection</h1>
        <div className="mb-4">
          <button 
            onClick={() => setActiveTab('live')}
            className={`px-4 py-2 ${activeTab === 'live' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-700'} rounded-tl-lg rounded-tr-lg`}
          >
            Home
          </button>
          <button 
            onClick={() => setActiveTab('upload')}
            className={`px-4 py-2 mx-3 ${activeTab === 'upload' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-700'} rounded-tl-lg rounded-tr-lg`}
          >
            Upload Image
          </button>
        </div>
        
        {activeTab === 'live' ? <LiveDetection /> : <ImageUpload />}
      </div>
    </div>
  );
}

export default App;
