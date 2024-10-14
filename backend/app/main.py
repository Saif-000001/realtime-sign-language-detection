import os
import cv2
import pickle
import numpy as np
import mediapipe as mp
import base64
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define paths for file uploads and processed files
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
PROCESSED_FOLDER = BASE_DIR / "processed"

# Create necessary directories
UPLOAD_FOLDER.mkdir(exist_ok=True)
PROCESSED_FOLDER.mkdir(exist_ok=True)

# Mount static files
app.mount("/processed", StaticFiles(directory=str(PROCESSED_FOLDER)), name="processed")

# Load the trained model
try:
    with open(BASE_DIR / "sign_language_model/model.h5", 'rb') as f:
        model_dict = pickle.load(f)
    model = model_dict['model']
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None  # Ensure model is None if loading fails

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Labels dictionary
labels_dict = {0: 'Hello', 1: 'I Love You', 2: 'Yes', 3: 'No', 4: 'Thanks'}

# List to store detected signs
detected_signs = []

# Function to process image and return prediction
def process_image(image_path):
    try:
        # Load the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            return None, "Error loading image."

        # Convert the image to RGB format
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if not results.multi_hand_landmarks:
            return None, "No hands detected in the image."

        data_aux = []
        for hand_landmarks in results.multi_hand_landmarks:
            x_ = []
            y_ = []

            # Process hand landmarks
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                data_aux.append(hand_landmarks.landmark[i].y - min(y_))

            # Attempt prediction with the loaded model
            try:
                prediction = model.predict([np.asarray(data_aux)])
                predicted_index = int(prediction[0])
                predicted_label = labels_dict.get(predicted_index, "Unknown label")
            except Exception as e:
                return None, f"Error during model prediction: {e}"

            # Draw the label on the image
            cv2.putText(img, predicted_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)

            # Save the processed image
            processed_image_path = PROCESSED_FOLDER / f'processed_{image_path.name}'
            cv2.imwrite(str(processed_image_path), img)

            return processed_image_path, predicted_label

        return None, "No hands detected."

    except Exception as e:
        logger.error(f"Error in process_image: {e}")
        return None, f"Error processing image: {e}"

# Image Upload Route
@app.post("/uploadfile/")
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Save the file to the upload folder
        file_path = UPLOAD_FOLDER / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process the image and get the result
        processed_image_path, label = process_image(file_path)
        
        if processed_image_path:
            return {
                "label": label,
                "image_path": f"/processed/{processed_image_path.name}"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to process image")
    
    except Exception as e:
        logger.error(f"Error processing file upload: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            image_data = base64.b64decode(data.split(",")[1])
            np_arr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            H, W, _ = img.shape

            # Process the image for hand landmarks
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks on the image
                    mp.solutions.drawing_utils.draw_landmarks(
                        img, 
                        hand_landmarks, 
                        mp_hands.HAND_CONNECTIONS)

                    # Prepare data for prediction
                    data_aux = []
                    x_ = []
                    y_ = []
                    
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                    # Make prediction
                    prediction = model.predict([np.asarray(data_aux)])
                    predicted_character = int(prediction[0])

                    # Store the predicted label
                    labels_dict = {0: 'Hello', 1: 'I Love You', 2: 'Yes', 3: 'No', 4: 'Thanks'}
                    detected_signs.append(labels_dict[predicted_character])

                    # Encode image to base64 for sending back to client
                    _, buffer = cv2.imencode('.jpg', img)
                    img_base64 = base64.b64encode(buffer).decode('utf-8')

                    # Send the result back to the client
                    await websocket.send_json({"image": img_base64, "label": labels_dict[predicted_character]})

            else:
                await websocket.send_json({"label": "No hands detected."})

        except Exception as e:
            await websocket.close()
            print(f"WebSocket error: {e}")
            break

@app.get("/detected_signs/")
async def get_detected_signs():
    for i in detected_signs:
        if detected_signs[i] == detected_signs[i+1]:
            return 
       
        return {"signs": detected_signs}

@app.get("/")
async def root():
    return {"message": "Welcome to the Sign Language Detection API"}
