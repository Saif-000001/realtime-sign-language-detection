
# 🖐️ Realtime-Sign-Language-Detection

## 🚀 Project Overview
This project is a Realtime-Sign-Language-Detection that contains the backend code for the Sign Language Detection application, implemented using FastAPI. It features MediaPipe for hand landmark detection and a trained machine learning model for sign recognition. The application supports both image uploads and live webcam feed for real-time sign language detection to text.

## Image Detection

![Hello Image](https://github.com/user-attachments/assets/7c10c077-4dd7-4743-8b0a-78d7868fe8e7)
![Processed Hello](https://github.com/user-attachments/assets/06c0744a-917a-491d-abe7-0f988497fdae)

### 📽️ Working Video Demonstration
[![Watch the video](https://github.com/user-attachments/assets/7c10c077-4dd7-4743-8b0a-78d7868fe8e7)](https://www.youtube.com/watch?v=4iQBZ6NNzMc&t=4s)




### Key Technologies:
- **Backend:** FastAPI
- **Frontend:** React + Vite
- **Machine Learning Model:** Random Forest Classifier for sign detection
- **Real-time Detection:** MediaPipe
- **Deployment:** Docker for containerization

## 🛠️ Setup and Installation
Follow these steps to set up and run the Realtime-Sign-Language-Detection locally.

## Project Structure
```plaintext
Realtime-Sign-Language-Detection/
├── backend/                  # Backend directory for server-side code
│   ├── app/                  # Application code
│   │   ├── __pycache__/      # Compiled Python files
│   │   ├── __init__.py       # Package initialization
│   │   └── main.py           # Main application file
│   ├── processed/            # Directory for processed images
│   ├── uploads/              # Directory for uploaded files
│   └── sign_language_detection/ # Directory for sign language detection models and scripts
│       ├── data/             # Data files directory
│       ├── collect_imgs.py    # Script to collect images
│       ├── create_dataset.py   # Script to create dataset
│       ├── data.pickle       # Pickled data file
│       ├── inference.py       # Inference script for the model
│       ├── model.h5          # Saved model file
│       ├── requirements.txt    # Requirements for model training
│       └── train_classifier.py  # Script to train the classifier
│   ├── .dockerignore         # Docker ignore file for backend
│   ├── .gitignore            # Git ignore file for backend
│   ├── Dockerfile            # Dockerfile for backend
│   └── requirements.txt       # Requirements for backend
├── frontend/                 # Frontend directory for client-side code
│   ├── node_modules/         # Node.js modules
│   ├── public/               # Public assets
│   ├── src/                  # Source files
│   │   ├── assets/           # Static assets
│   │   ├── components/       # React components
│   │   │   ├── ImageUploader/ # Component for image uploading
│   │   │   └── LiveDetection/ # Component for live detection
│   │   ├── App.css           # Main CSS file
│   │   ├── App.jsx           # Main React component
│   │   ├── index.css         # Global CSS styles
│   │   └── main.jsx          # Entry point for React application
│   ├── .dockerignore         # Docker ignore file for frontend
│   ├── .gitignore            # Git ignore file for frontend
│   ├── Dockerfile            # Dockerfile for frontend
│   ├── .eslintrc.cjs         # ESLint configuration file
│   ├── index.html            # Main HTML file
│   ├── package-lock.json     # Lock file for npm dependencies
│   ├── package.json          # npm configuration file
│   ├── postcss.config.js     # PostCSS configuration file
│   ├── README.md             # Frontend README file
│   ├── tailwind.config.js     # Tailwind CSS configuration file
│   └── vite.config.js        # Vite configuration file
├── .dockerignore         # Docker ignore file 
├── .gitignore            # Git ignore file 
├── docker-compose.yml        # Docker Compose configuration file

```

### 1. Clone the Repository
First, clone the repository from GitHub:

```bash
git clone https://github.com/Saif-000001/Realtime-Sign-Language-Detection.git
cd Realtime-Sign-Language-Detection
```
Open your project a new terminal. In the terminal, navigate to the frontend directory using the command `cd frontend`, and then install the project dependencies by running `npm install`. 

#### 2. Build and Run the Docker Containers

```bash
docker-compose up --build
```
This command builds the images for the frontend and backend if they don't exist and starts the containers. The backend is available at `http://localhost:8000/` and the frontend at `http://localhost:5173/`.

#### 3. Viewing the Application

Open a browser and navigate to `http://localhost:5173/` to view the React application. It should display a message fetched from the FastAPI backend.

## Stopping the Application
To stop the application and remove containers, networks, and volumes created by `docker-compose up`, you can use:

```bash 
docker-compose down -v
```

## 🧠 Key Learnings
- Data collection and preprocessing techniques for machine learning.
- Model training and optimization strategies.
- Building efficient backend services with FastAPI.
- Creating dynamic frontend applications with React.
- Basics of Docker for application containerization.
- Understanding end-to-end project architecture and data flow.

## 💡 Challenges Overcome
- Balancing dataset quality and quantity.
- Integrating the machine learning model with the web application.
- Implementing real-time communication between the frontend and backend.
- Ensuring consistent deployment across different environments.

## 🙏 Acknowledgements
I’m grateful for the support from various online communities, tutorials, and documentation resources that helped me throughout this project!
