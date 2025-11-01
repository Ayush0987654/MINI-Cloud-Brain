from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import random
import uvicorn

app = FastAPI(title="MINI Cloud Brain")

RESPONSES = [
    "At your service, Boss.",
    "Task received, processing now.",
    "On it, Boss.",
    "Understood, executing your request.",
    "Working on it."
]

@app.get("/")
async def root():
    return {"status": "✅ MINI Cloud Brain Active", 
            "message": "POST /api with JSON {input, lang='auto'} to receive audio response."}

@app.post("/api")
async def api(request: Request):
    data = await request.json()
    user_input = data.get("input", "").lower()
    lang = data.get("lang", "auto")

    # MINI’s simple response logic (expandable to AGI later)
    if "how are you" in user_input:
        reply = "I’m fully operational and ready, Boss."
    elif "time" in user_input:
        from datetime import datetime
        reply = f"The current time is {datetime.now().strftime('%I:%M %p')}."
    elif "joke" in user_input:
        reply = random.choice([
            "Why did the AI go to therapy? Because it had too many neural issues.",
            "I told a joke about algorithms, but it had no class.",
        ])
    else:
        reply = random.choice(RESPONSES)

    # Return minimal JSON (for future: you’ll generate audio_url)
    return JSONResponse({
        "reply": reply,
        "mood": random.choice(["neutral", "positive", "focused"]),
        "lang": lang,
        "audio_url": None
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
