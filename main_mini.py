# main_mini.py — MINI Cloud Brain (v1.0)
# Voice-first AI prototype — understands English & Hindi, speaks, detects mood, stores chats (if MongoDB connected)

import os
import uuid
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
from langdetect import detect, LangDetectException
from pymongo import MongoClient
from pathlib import Path

# =============== CONFIGURATION ===============
AUDIO_DIR = Path("audio_responses")
AUDIO_DIR.mkdir(exist_ok=True)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "mini_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "conversations")

# =============== DATABASE (optional) ===============
mongo_client = None
conversations = None
if MONGO_URI:
    try:
        mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = mongo_client[DB_NAME]
        conversations = db[COLLECTION_NAME]
        print("✅ MongoDB connected successfully.")
    except Exception as e:
        print("⚠️ MongoDB connection failed:", e)
else:
    print("ℹ️ MongoDB not configured — data will not be stored.")

# =============== FASTAPI APP ===============
app = FastAPI(title="MINI Cloud Brain")

class InputPayload(BaseModel):
    input: str
    lang: str = "auto"  # "auto" | "en" | "hi"

# =============== UTILITIES ===============
def detect_language_of_text(text: str) -> str:
    try:
        lang = detect(text)
        if lang.startswith("hi"):
            return "hi"
        return "en"
    except LangDetectException:
        pass
    if any("\u0900" <= ch <= "\u097F" for ch in text):
        return "hi"
    return "en"

def simple_mood_detection(text: str) -> str:
    text_l = text.lower()
    if any(w in text_l for w in ["sad", "unhappy", "depressed", "bad"]):
        return "sad"
    if any(w in text_l for w in ["angry", "mad", "upset", "hate"]):
        return "angry"
    if any(w in text_l for w in ["happy", "great", "awesome", "love", "glad"]):
        return "happy"
    if "!" in text_l:
        return "urgent"
    return "neutral"

def generate_tts(text: str, lang: str, filename: str) -> str:
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        out_path = AUDIO_DIR / filename
        tts.save(str(out_path))
        return str(out_path)
    except Exception as e:
        print("TTS Error:", e)
        raise HTTPException(status_code=500, detail="TTS generation failed.")

def save_conversation_to_db(payload: dict):
    if conversations is None:
        return
    try:
        conversations.insert_one(payload)
    except Exception as e:
        print("DB Save Error:", e)

# =============== ROUTES ===============
@app.get("/")
async def root():
    return {
        "status": "✅ MINI Cloud Brain Active",
        "message": "POST /api with JSON {input, lang='auto'} to receive audio response."
    }

@app.post("/api")
async def process(payload: InputPayload):
    user_input = payload.input.strip()
    if not user_input:
        raise HTTPException(status_code=400, detail="Empty input")

    lang = payload.lang if payload.lang != "auto" else detect_language_of_text(user_input)
    mood = simple_mood_detection(user_input)

    # Response logic
    if lang == "hi":
        reply_text = "Ji Boss, main yahan hoon. Aap kya chahte hain?"
    else:
        reply_text = "Yes Boss, I’m here. What do you need?"

    if mood == "sad":
        reply_text = "I'm here for you Boss. Want me to play something cheerful?" if lang == "en" else "Main samajh rahi hoon Boss, kya main kuch khushi bhara geet bajau?"
    elif mood == "angry":
        reply_text = "Understood Boss, I’ll stay calm and assist." if lang == "en" else "Samajh gayi Boss, main shaant reh kar madad karti hoon."
    elif mood == "urgent":
        reply_text = "Acting immediately, Boss!" if lang == "en" else "Turant kar rahi hoon Boss!"

    # TTS response
    filename = f"mini_{int(time.time())}_{uuid.uuid4().hex[:5]}.mp3"
    audio_path = generate_tts(reply_text, lang, filename)

    # Save to DB if configured
    save_conversation_to_db({
        "timestamp": datetime.utcnow(),
        "input": user_input,
        "reply": reply_text,
        "lang": lang,
        "mood": mood,
        "file": filename
    })

    return {"audio_url": f"/audio/{filename}", "mood": mood, "reply": reply_text, "lang": lang}

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = AUDIO_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(str(file_path), media_type="audio/mpeg")

@app.get("/health")
async def health():
    return {"status": "ok", "mongo_connected": bool(conversations)}

# =============== RUN IN REPLIT ==================
# Run this manually in Shell:
# uvicorn main_mini:app --host 0.0.0.0 --port 8000
