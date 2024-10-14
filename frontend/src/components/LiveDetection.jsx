import React, { useState, useRef, useEffect } from 'react';

function LiveDetection() {
  const [isWebcamActive, setIsWebcamActive] = useState(false);
  const [detectedSigns, setDetectedSigns] = useState([]);
  const videoRef = useRef(null);
  const wsRef = useRef(null);

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      setIsWebcamActive(true);
      startWebSocket();
    } catch (error) {
      console.error('Error accessing the webcam:', error);
    }
  };

  const stopWebcam = () => {
    if (videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setIsWebcamActive(false);
      setDetectedSigns([]);
      if (wsRef.current) {
        wsRef.current.close();
      }
    }
  };

  const startWebSocket = () => {
    wsRef.current = new WebSocket('ws://localhost:8000/ws');
    wsRef.current.onopen = () => console.log('WebSocket connected');
    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.label && data.label !== "No hands detected.") {
        addDetectedSign(data.label);
      }
    };
    wsRef.current.onerror = (error) => console.error('WebSocket error:', error);
    wsRef.current.onclose = () => console.log('WebSocket disconnected');

    setInterval(() => {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        const canvas = document.createElement('canvas');
        canvas.width = videoRef.current.videoWidth;
        canvas.height = videoRef.current.videoHeight;
        canvas.getContext('2d').drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
        canvas.toBlob((blob) => {
          const reader = new FileReader();
          reader.onload = () => {
            wsRef.current.send(reader.result);
          };
          reader.readAsDataURL(blob);
        }, 'image/jpeg');
      }
    }, 100);
  };

  const addDetectedSign = (label) => {
    setDetectedSigns(prevSigns => {
      if (prevSigns.length === 0 || prevSigns[prevSigns.length - 1] !== label) {
        return [...prevSigns, label];
      }
      return prevSigns;
    });
  };

  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <div className="flex items-start">
      {/* Webcam feed */}
      <div className="w-1/2 mr-4">
        <div className="mb-4">
          {!isWebcamActive ? (
            <button onClick={startWebcam} className="bg-green-500 text-white px-4 py-2 rounded">
              Start Webcam
            </button>
          ) : (
            <button onClick={stopWebcam} className="bg-red-500 text-white px-4 py-2 rounded">
              Stop Webcam
            </button>
          )}
        </div>
        <div className="relative">
          <video ref={videoRef} className="w-full h-auto mb-4" autoPlay></video>
        </div>
      </div>
      <div className="w-1/2">
        {/* <h4>Detected signs</h4> */}
        <ul className="text-lg text-center">
          {detectedSigns.map((sign, index) => (
            <li key={index}>
              <input
                type="text"
                className="border px-2 py-1 w-full text-center"
                value={sign}
                readOnly
              />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default LiveDetection;
