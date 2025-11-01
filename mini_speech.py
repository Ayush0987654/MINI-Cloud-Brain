# mini_speech.py — MINI Voice Interface (v1.0)
# Connects with main_mini.py on localhost:8000 and handles speech input/output

import speech_recognition as sr
import pyttsx3
import requests
import json
import time

API_URL = "http://localhost:8000/api"

r = sr.Recognizer()
engine = pyttsx3.init()

# Choose UK Female voice if available
voices = engine.getProperty('voices')
for v in voices:
    if "Hazel" in v.name or "Zira" in v.name or "English" in v.name:
        engine.setProperty('voice', v.id)
engine.setProperty('rate', 175)

def speak(text):
    print(f"MINI: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"YOU: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that Boss.")
        return ""
    except sr.RequestError:
        speak("Speech service is not responding.")
        return ""

def process_command(cmd):
    payload = {"input": cmd, "lang": "auto"}
    try:
        res = requests.post(API_URL, json=payload)
        data = json.loads(res.text)
        reply = data.get("reply", "")
        speak(reply)
    except Exception as e:
        print("Error:", e)
        speak("Could not reach the cloud brain right now.")

if __name__ == "__main__":
    speak("Hello Boss, MINI is online and listening.")
    while True:
        query = listen().lower()
        if "stop" in query or "sleep" in query or "goodbye" in query:
            speak("Going offline Boss. See you soon.")
            break
        elif query:
            process_command(query)
        time.sleep(0.4)
