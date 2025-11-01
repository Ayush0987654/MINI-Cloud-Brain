import speech_recognition as sr
import pyttsx3
import requests
import json
import time

# ✅ MINI Cloud Brain endpoint (Replit link)
API_URL = "https://2a61a383-a1eb-4f53-9149-7793d469704f-00-zd3ljsgy1lp7.sisko.replit.dev/api"

# Initialize recognizer and voice engine
r = sr.Recognizer()
engine = pyttsx3.init()

# 🎙️ Voice setup — British female (closest to Friday)
voices = engine.getProperty('voices')
for v in voices:
    if "Hazel" in v.name or "Zira" in v.name or "Samantha" in v.name:
        engine.setProperty('voice', v.id)
engine.setProperty('rate', 175)

def speak(text):
    """MINI’s voice output"""
    print(f"MINI: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """MINI’s ears — listens to user speech"""
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.adjust_for_ambient_noise(source, duration=0.8)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"YOU: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that, Boss.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service failed.")
        return ""

def process_command(cmd):
    """Send command to MINI Cloud Brain and speak response"""
    payload = {"input": cmd, "lang": "auto"}
    try:
        res = requests.post(API_URL, json=payload)
        if res.status_code == 200:
            data = res.json()
            reply = data.get("reply", "I didn’t understand that.")
            mood = data.get("mood", "")
            speak(f"{reply} (Mood: {mood})")
        else:
            speak("I couldn’t reach my Cloud Brain.")
    except Exception as e:
        speak("Connection error.")
        print("Error:", e)

if __name__ == "__main__":
    speak("Hello Boss, MINI is online and listening.")
    while True:
        query = listen().lower()
        if query in ["stop", "sleep", "goodbye", "shutdown"]:
            speak("Going offline, Boss.")
            break
        elif query:
            process_command(query)
        time.sleep(0.4)
