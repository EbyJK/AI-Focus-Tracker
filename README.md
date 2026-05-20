# 🎯 AI Focus Tracker

An advanced real-time concentration and fatigue monitoring system built using **Python, OpenCV, and MediaPipe Face Mesh**.

This project tracks:
- 👀 Eye gaze
- 🧠 Focus levels
- 😴 Fatigue indicators
- 📈 Attention trends
- 🎯 Confidence stability
- 🫥 Blink activity

and visualizes everything through a modern AI-style dashboard UI.

---

# 🚀 Features

## ✅ Real-Time Face Tracking
- MediaPipe Face Mesh integration
- 468 facial landmarks
- Live face mesh rendering

---

## ✅ Personalized Focus Calibration
The system calibrates:
- your natural head position
- your neutral gaze direction
- personalized attention baseline

This improves:
- accuracy
- stability
- realism

---

## ✅ Intelligent Focus Scoring
Focus score is calculated using:
- gaze tracking
- head pose estimation
- blink activity
- temporal smoothing

Focus states:
- 🔥 Deep Focus
- ✅ Focused
- ⚠️ Drifting
- ❌ Distracted

---

## ✅ Stability Engine
The system uses:
- exponential smoothing
- confidence accumulation
- temporal stabilization

to avoid noisy and jittery scoring.

---

## ✅ Fatigue Detection Engine
Tracks:
- prolonged low focus
- excessive blinking
- low confidence states

Provides:
- fatigue estimation
- warning system
- break recommendations

---

## ✅ Live Dashboard UI
Modern AI-inspired dashboard built using OpenCV.

Includes:
- dynamic cards
- responsive layout
- animated focus ring
- real-time graph
- live analytics
- status indicators

---

## ✅ Attention Heatmap
Visualizes:
- gaze movement
- attention regions
- concentration zones

using live heatmap overlays.

---

## ✅ Session Analytics
Tracks:
- average focus
- distraction count
- session duration
- confidence levels

---

# 🖥️ Dashboard Preview

Features visible in UI:
- AI Focus Score
- Focus State
- Blink Detection
- Confidence Meter
- Fatigue State
- Live Trend Graph
- Circular Focus Ring
- Attention Heatmap
- Session Analytics

---

# 🛠️ Tech Stack

## Core Technologies
- Python
- OpenCV
- NumPy
- MediaPipe

---

## Computer Vision
- Face Mesh Tracking
- Eye Gaze Estimation
- Head Pose Tracking
- Blink Detection

---

## UI System
Custom dashboard built entirely using:
- OpenCV drawing APIs
- layered rendering
- dynamic visualization

---

# 📂 Project Structure

```bash
concentration_tracker/
│
├── concen_tracker.py     # Main application
├── ui.py                 # Dashboard rendering
├── theme.py              # Colors & UI styling
├── tracker.py            # Tracking utilities
├── analytics.py          # Fatigue & confidence engine
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-focus-tracker.git
cd ai-focus-tracker
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows
```bash
venv\Scripts\activate
```

### Linux/Mac
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Requirements

```txt
opencv-python
mediapipe
numpy
```

---

# ▶️ Run Application

```bash
python concen_tracker.py
```

---

# 🧠 System Architecture

## Focus Pipeline

```text
Webcam Feed
    ↓
Face Mesh Detection
    ↓
Gaze + Head Pose Analysis
    ↓
Focus Scoring
    ↓
Stability Engine
    ↓
Fatigue Detection
    ↓
Dashboard Visualization
```

---

# 🎨 UI Components

## Left Panel
- Focus Score
- Status
- Blink State
- Confidence
- Fatigue State

---

## Main Area
- Webcam Feed
- Face Mesh Overlay
- Attention Heatmap

---

## Bottom Analytics
- Focus Trend Graph
- Circular Focus Ring
- Session Analytics
- Live Status Indicator

---

# 📈 Future Improvements

Planned upgrades:
- PyQt Desktop Application
- Data Persistence
- Session Exporting
- ML-based Attention Classification
- Productivity Reports
- Emotion Detection
- Multi-user Profiles
- Cloud Analytics Dashboard

---

# 🧪 Current Capabilities

✅ Real-time focus tracking  
✅ Personalized calibration  
✅ Adaptive scoring  
✅ Stability modeling  
✅ Fatigue estimation  
✅ Attention heatmaps  
✅ Dynamic dashboard UI  
✅ Session analytics  

---

# 📸 Screenshots

_Add screenshots of your dashboard here_

```markdown
![Dashboard](screenshots/dashboard.png)
```

---

# 🤝 Contributing

Contributions, ideas, and improvements are welcome.

Feel free to:
- fork the project
- create pull requests
- suggest features
- improve algorithms

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Built with ❤️ using Python, OpenCV, and MediaPipe.