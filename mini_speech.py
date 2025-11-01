# ======================================
# MINI Speech Interface (mini_speech.py)
# ======================================

import speech_recognition as sr
import requests
import json
import time
import os
from playsound import playsound

# ------------------------------------------------------
#  ✅ MINI Configuration
# ------------------------------------------------------

# Replace this with your active Replit API endpoint:
API_URL = "https://2a61a383-a1eb-4f53-9149-7793d469704f-00-zd3ljsgy1lp7.sisko.replit.dev/api"

# Path to MINI’s unique Friday-like voice sample (MP4/MP3)
VOICE_SAMPLE_PATH = os.path.join("assets", "voices", "friday_voice.mp4")

# Temporary file where downloaded audio (if returned from cloud) will be stored
TEMP_AUDIO_PATH = os.path.join("assets", "temp_output.mp3")

# Speech Recognizer initialization
r = sr.Recognizer()

# ------------------------------------------------------
#  🗣️ Voice System (Offline Playback)
# ------------------------------------------------------

def speak(text: str):
    """
    Convert MINI's reply to speech.
    Uses predefined Friday-like audio sample or fallback text.
    """
    print(f"MINI 🎧: {text}")
    # For now, plays Friday sample to symbolize MINI speaking.
    # Later, this can be replaced with a cloned voice synthesis function.
    if os.path.exists(VOICE_SAMPLE_PATH):
        playsound(VOICE_SAMPLE_PATH)
    else:
        print("[⚠️] Friday voice sample missing. Please add it under assets/voices/.")

# ------------------------------------------------------
#  🎧 Listening System
# ------------------------------------------------------

def listen() -> str:
    """
    Listens to your command through microphone and transcribes it.
    """
    with sr.Microphone() as source:
        print("\n🎙️ Listening Boss...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        print(f"YOU 🧍‍♂️: {query}")
        return query
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that Boss.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is offline, Boss.")
        return ""

# ------------------------------------------------------
#  🧩 Brain Communication
# ------------------------------------------------------

def process_command(command: str):
    """
    Sends text command to MINI Cloud Brain, processes response.
    """
    payload = {"input": command, "lang": "auto"}
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        data = response.json()
        reply = data.get("reply", "I didn’t understand that.")
        audio_url = data.get("audio_url")

        mood = data.get("mood", "neutral")
        speak(f"(Mood: {mood})")

        if audio_url:
            # If MINI returns a dynamic audio file, download & play it
            audio_data = requests.get(audio_url)
            with open(TEMP_AUDIO_PATH, "wb") as f:
                f.write(audio_data.content)
            playsound(TEMP_AUDIO_PATH)
        else:
            speak(reply)

    except Exception as e:
        print("[ERROR] Could not connect to MINI Cloud Brain:", e)
        speak("Could not reach the cloud brain, Boss. Reconnecting...")

# ------------------------------------------------------
#  🚀 MAIN EXECUTION LOOP
# ------------------------------------------------------

if __name__ == "__main__":
    print("=====================================")
    print("     🧠 MINI Speech Module Online    ")
    print("=====================================\n")
    speak("Hello Boss, MINI is online and listening.")

    while True:
        command = listen().lower()
        if command in ["stop", "sleep", "goodbye", "shutdown"]:
            speak("Going offline Boss.")
            break
        elif command:
            process_command(command)
        time.sleep(0.6)
