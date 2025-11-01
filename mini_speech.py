import speech_recognition as sr
import pyttsx3
import requests
import json
import time

# ✅ MINI Cloud Brain (Replit) endpoint
API_URL = "https://2a61a383-a1eb-4f53-9149-7793d469704f-00-zd3ljsgy1lp7.sisko.replit.dev/api"

# Initialize engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Voice setup (UK English, like Friday)
voices = engine.getProperty('voices')
for v in voices:
    if "Hazel" in v.name or "Zira" in v.name:
        engine.setProperty('voice', v.id)
engine.setProperty('rate', 175)

def speak(text):
    print("MINI:", text)
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
        speak("Sorry, I didn’t catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service error.")
        return ""

def process_command(cmd):
    payload = {"input": cmd, "lang": "auto"}
    try:
        res = requests.post(API_URL, json=payload)
        data = json.loads(res.text)
        audio_url = data.get("audio_url")
        mood = data.get("mood", "")
        lang = data.get("lang", "")
        speak(f"(Mood: {mood})")
        if audio_url:
            speak("Done, boss.")
        else:
            speak(data.get("reply", "I didn’t understand that."))
    except Exception as e:
        speak("Could not reach the cloud brain.")
        print("Error:", e)

if __name__ == "__main__":
    speak("Hello Boss, MINI is online and listening.")
    while True:
        query = listen().lower()
        if "stop" in query or "sleep" in query or "goodbye" in query:
            speak("Going offline Boss.")
            break
        elif query:
            process_command(query)
        time.sleep(0.5)
