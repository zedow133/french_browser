# French Browser

A video search and analysis application that allows users to search through video content using textual queries and browse keyframes with similarity matching.

## 📋 Prerequisites

Before installing the application, ensure you have the following installed on your system:

- **Node.js**
- **Python**
- **Angular CLI**
- **ffmpeg**

## 🛠️ Installation

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd ./backend/
   ```

2. **Create and activate a Python virtual environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install TransNetV2**:
   ```bash
   cd ./TransNetV2/
   python setup.py install
   cd ..
   ```

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd ./frontend/
   ```

2. **Install project dependencies**:
   ```bash
   npm install
   ```

## 🚀 Running the Application

### 1. Generate Database

> ### ⚠️ **WARNING**
> The generation of the database can take a very long time, especially when using **CPU**.  
> It is advised to use the following link to [download the database](https://filesender.renater.fr/?s=download&token=8fc3e510-0b0a-4c77-bb3e-ebfacf75726c&lang=en)  
> Once downloaded, add the folder to the application backend and directly start the backend server.

If not downloaded, generate a database from your video files:

```bash
# Navigate to backend directory
cd ./backend/

# Put all your videos in a directory, then run:
python generate_db.py <video_directory_name>
```

This will create a `db` folder containing the processed video database.

### 2. Start the Backend Server

```bash
# Make sure you're in the backend directory and virtual environment is activated
python server.py
```

The backend server will start on **port 8000**.

### 3. Start the Frontend

In a new terminal window:

```bash
# Navigate to frontend directory
cd ./frontend/

# Start the Angular development server
ng serve
```

The frontend will start on **port 4200**.

### 4. Access the Application

Open your web browser and navigate to:
```
http://localhost:4200
```

## 📖 How to Use

### Getting Started

1. **Access the Application**: Open your browser and go to `http://localhost:4200`
2. **Homepage**: You'll see the French Browser interface with a search panel on the left

### Searching Videos

1. **Enter Your Query**: Type your search term in the query input field
2. **Execute Search**: Click the "Search" button to find relevant keyframes
3. **Reset Search**: Use "Reset Search" to clear results and start over

### Viewing Results

- **Browse Keyframes**: Search results appear on the right, ordered by similarity (up to 100 keyframes)
- **Select Keyframe**: Click on any keyframe to view the corresponding video

### Video Player Features

When you select a keyframe, you'll access:

- **Video Playback**: The video starts at the selected keyframe's timestamp
- **Timeline Control**: Manually adjust start and end timestamps
- **Clip Navigation**: Use "Go to clip start" to return to the beginning of the clip
- **Related Content**: View similar keyframes and clips from the same segment
- **Submission**: Submit your selection when ready

### Navigation

- **Return Home**: Click "French Browser" in the header at any time to return to the homepage
- **New Search**: Start fresh searches from the homepage

## 🤝 Contributing

Léo DE SOUSA DUFFY (ledesousaduf@edu.aau.at)
Samantha TISSIER (satissier@edu.aau.at)
