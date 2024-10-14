import React, { useState } from 'react';

function ImageUpload() {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [detectedSign, setDetectedSign] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    try {
      const response = await fetch('http://localhost:8000/uploadfile/', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      setUploadedImage(`http://localhost:8000${result.image_path}`);
      setDetectedSign(result.label);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="mb-4">
        <input type="file" name="file" accept="image/*" className="mb-2" required />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Upload and Detect
        </button>
      </form>

      {/* Flexbox container to display the image and detected sign side by side */}
      <div className="flex items-start justify-center">
        {/* Uploaded Image */}
        {uploadedImage && (
          <div className="w-75% mr-4">
            <img src={uploadedImage} alt="Uploaded" className="w-full h-auto" />
          </div>
        )}

        {/* Detected Sign */}
        {detectedSign && (
          <div className="w-1/2 mt-5 text-center">
            <div className="text-xl font-bold">Detected Sign:</div>
            <div className="text-2xl text-red-500">{detectedSign}</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ImageUpload;
