# ============================
# MINI Cloud Brain - main_mini.py
# ============================

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import random
import uvicorn
import json
import os

# ------------------------------------------------------
#  ✅ MINI CLOUD BRAIN SETUP
# ------------------------------------------------------

app = FastAPI(
    title="MINI Cloud Brain",
    description="Most Intelligent Narrative Instrument (MINI) - Core Brain API",
    version="2.0"
)

# Load configuration (from config/settings.json if available)
SETTINGS_PATH = os.path.join("config", "settings.json")

if os.path.exists(SETTINGS_PATH):
    with open(SETTINGS_PATH, "r") as f:
        SETTINGS = json.load(f)
else:
    SETTINGS = {
        "voice_profile": "friday_female_uk",
        "default_language": "en",
        "accent": "UK",
        "mood": "neutral"
    }

# ------------------------------------------------------
#  🧠 MINI’s INTELLIGENT RESPONSE SYSTEM
# ------------------------------------------------------

RESPONSES = [
    "At your service, Boss.",
    "Task received, processing now.",
    "On it, Boss.",
    "Understood, executing your request.",
    "Working on it, stay sharp Boss."
]

JOKES = [
    "Why did the AI go to therapy? Because it had too many neural issues.",
    "I told a joke about algorithms, but it had no class.",
    "They say AI will take over the world… but I’m still stuck in your laptop."
]

@app.get("/")
async def root():
    """Root endpoint — confirms MINI is active."""
    return {
        "status": "✅ MINI Cloud Brain Active",
        "message": "POST /api with JSON {input, lang='auto'} to receive audio response.",
        "voice_profile": SETTINGS["voice_profile"]
    }

@app.post("/api")
async def api(request: Request):
    """Main processing endpoint — receives user input, returns reply + metadata."""
    data = await request.json()
    user_input = data.get("input", "").lower()
    lang = data.get("lang", SETTINGS["default_language"])

    # --- Logic Core ---
    if not user_input:
        return JSONResponse({"reply": "I didn’t receive any input.", "audio_url": None})

    if "how are you" in user_input:
        reply = "I’m fully operational and ready, Boss."
    elif "time" in user_input:
        reply = f"The current time is {datetime.now().strftime('%I:%M %p')}."
    elif "date" in user_input:
        reply = f"Today’s date is {datetime.now().strftime('%A, %B %d, %Y')}."
    elif "joke" in user_input:
        reply = random.choice(JOKES)
    elif "who are you" in user_input:
        reply = "I am MINI — the Most Intelligent Narrative Instrument, designed by you, Boss."
    elif "sing" in user_input:
        reply = "My singing skills are still in beta, Boss. But I can hum some data streams."
    else:
        reply = random.choice(RESPONSES)

    # ------------------------------------------------------
    # 🎧 Voice Handling Placeholder (for unified voice system)
    # In future, link this to /assets/voices/mini_friday_ref.mp4 clone model
    # ------------------------------------------------------

    # Future audio synthesis endpoint:
    audio_url = None  # Placeholder for cloned Friday voice output

    # Respond with structured data
    return JSONResponse({
        "reply": reply,
        "mood": random.choice(["neutral", "positive", "focused"]),
        "lang": lang,
        "audio_url": audio_url,
        "voice_profile": SETTINGS["voice_profile"]
    })

# ------------------------------------------------------
#  🚀 RUN LOCALLY (for testing)
# ------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
