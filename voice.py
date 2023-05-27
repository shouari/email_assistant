import time

import pyttsx3
import speech_recognition as sr


def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')

    engine.setProperty('rate', 200)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.say(text)
    engine.runAndWait()
    return

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio_text = r.listen(source)
        time.sleep(2)

        try:
            text = r.recognize_google(audio_text)
            print(f"You said: {text}")
        except:
            speak("Sorry, I didn't get that")
