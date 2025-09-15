# AIMockInterviwer

# 🧑‍💻 AI Mock Interviewer (Excel Focused)

An **AI-powered mock interview platform** that simulates an Excel interview.  
Built with **React (frontend)** + **FastAPI (backend)** + **Gemini API**.  

The system conducts staged interviews (Easy → Medium → Hard), evaluates responses, and generates a **performance summary** at the end.

---

## 🚀 Live Demo
- **Frontend (Vercel):** [https://ai-mock-interviewer-blbu.vercel.app](https://ai-mock-interviewer-blbu.vercel.app)  
- **Backend (Render):** [https://aimockinterviwer-excelrelated.onrender.com](https://aimockinterviwer-excelrelated.onrender.com)

---

## ✨ Features
- Chat-based **interactive Excel interview**.  
- **Staged difficulty**: Easy → Medium → Hard.  
- AI provides **light feedback** without revealing answers.  
- Generates structured **Performance Summary**:
  - Score (X/10)  
  - Strengths  
  - Areas to Improve  
  - Final Remark  
- **Typing effect** for natural AI responses.  
- Stores transcripts for later review.  

---

## 🛠️ Tech Stack
- **Frontend:** React, Axios, CSS  
- **Backend:** FastAPI (Python), Pydantic  
- **AI Model:** Google Gemini API  
- **Deployment:** Vercel (Frontend), Render (Backend)  

---

## 📂 Project Structure
AI_Mock_Interviewer/
│
├── backend/ # FastAPI backend
│ ├── app.py # Main backend app
│ ├── requirements.txt
│ └── transcripts/ # Stores session transcripts
│
├── frontend/ # React frontend
│ ├── src/
│ │ └── App.js
│ ├── package.json
│ └── index.css
│
└── README.md


---

## ⚡ Getting Started (Local Setup)

### 1️⃣ Clone the repo
```bash
git clone https://github.com/ankitlochantiwary/AI_Mock_Interviewer.git
cd AI_Mock_Interviewer


## 2️⃣ Backend Setup (FastAPI)
cd backend
python -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows

pip install -r requirements.txt


Create .env file in backend/:

GEMINI_KEY=your_gemini_api_key_here


Run backend:

uvicorn backend.app:app --reload --port 8000


Backend available at → http://127.0.0.1:8000/docs

## 3️⃣ Frontend Setup (React)
cd frontend
npm install


Create .env file in frontend/:

REACT_APP_BACKEND=http://127.0.0.1:8000


Run frontend:

npm start


Frontend available at → http://localhost:3000
