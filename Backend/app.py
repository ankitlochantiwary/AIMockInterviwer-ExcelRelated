# backend/app.py

import os
import uuid
import json
import google.generativeai as genai
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -------------------------
# Direct Gemini API Key
# -------------------------
GEMINI_KEY = "AIzaSyARc4djjBkyU5Dow-vmoaQTL-Ru3Q_yjQo"

if not GEMINI_KEY:
    raise ValueError("❌ Please provide a Gemini API key")

genai.configure(api_key=GEMINI_KEY)

TRANSCRIPTS_DIR = "transcripts"
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

# -------------------------
# FastAPI app
# -------------------------
app = FastAPI(title="AI Excel Mock Interviewer (Gemini)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# -------------------------
# Session store
# -------------------------
SESSIONS: Dict[str, Dict[str, Any]] = {}

# -------------------------
# Request models
# -------------------------
class StartResp(BaseModel):
    session_id: str
    question: str

class AnswerReq(BaseModel):
    session_id: str
    answer: str

class LogEventReq(BaseModel):
    session_id: str
    event_type: str
    details: Optional[str] = None

# -------------------------
# Utilities
# -------------------------
def _create_session() -> Dict[str, Any]:
    sid = str(uuid.uuid4())
    session = {
        "id": sid,
        "stage": 0,  # 0 = easy, 1 = medium, 2 = hard
        "history": [],
        "answers": [],
        "security_events": [],
        "created_at": datetime.utcnow().isoformat()
    }
    SESSIONS[sid] = session
    return session

def _get_session(sid: str) -> Dict[str, Any]:
    s = SESSIONS.get(sid)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return s

def _save_transcript(session: Dict[str, Any]) -> str:
    path = os.path.join(TRANSCRIPTS_DIR, f"transcript_{session['id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2, default=str)
    return path

def ask_gemini(prompt: str) -> str:
    """Send prompt to Gemini and return text."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 400}
        )
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini error:", e)
        return f"(Error asking Gemini: {e})"

# -------------------------
# API endpoints
# -------------------------
@app.post("/start", response_model=StartResp)
def start_interview():
    session = _create_session()
    prompt = """You are an AI interviewer for Excel skills.
1. Start with a warm, short greeting.
2. Briefly explain the process (easy → harder).
3. Ask the FIRST EASY Excel question clearly.
Keep it natural and conversational."""
    question = ask_gemini(prompt)
    session["history"].append({"role": "assistant", "content": question})
    return {"session_id": session["id"], "question": question}

@app.post("/answer")
async def submit_answer(req: AnswerReq):
    session = _get_session(req.session_id)
    session["history"].append({"role": "user", "content": req.answer})
    session["answers"].append(req.answer)

    transcript = "\n".join([f"{h['role']}: {h['content']}" for h in session["history"]])
    stage = ["EASY", "MEDIUM", "HARD"][min(session["stage"], 2)]

    prompt = f"""
You are an AI Excel interviewer. Maintain a professional, supportive tone.

Transcript so far:
{transcript}

Now follow these rules:
1. If the candidate asks YOU a question, answer politely but briefly.
2. If the candidate gave an interview answer, acknowledge or give light feedback 
   (but do NOT reveal the full correct answer).
3. Then continue by asking the NEXT {stage} Excel interview question (if any left).
4. If it's the end, provide a short, professional closing message.
"""
    reply = ask_gemini(prompt)
    session["history"].append({"role": "assistant", "content": reply})

    if not req.answer.strip().endswith("?") and session["stage"] < 2:
        session["stage"] += 1
        return {"next_question": reply}
    else:
        return {"message": reply}

@app.post("/log_event")
async def log_event(req: LogEventReq):
    session = _get_session(req.session_id)
    ev = {"type": req.event_type, "details": req.details, "time": datetime.utcnow().isoformat()}
    session["security_events"].append(ev)
    _save_transcript(session)
    return {"status": "logged", "event": ev}

@app.get("/summary")
def get_summary(session_id: str):
    session = _get_session(session_id)
    transcript = "\n".join([f"{h['role']}: {h['content']}" for h in session["history"]])

    prompt = f"""You are an interview evaluator. Here is the transcript of a mock Excel interview:

{transcript}

Now create a performance summary in this **exact plain-text format** (no Markdown, no asterisks, no bullet dashes):

Performance Summary
Score: X/10
Strengths:
1. ...
2. ...
Areas to Improve:
1. ...
2. ...
Final Remark:
..."""

    summary = ask_gemini(prompt)
    _save_transcript(session)
    return {"session_id": session["id"], "summary": summary}

