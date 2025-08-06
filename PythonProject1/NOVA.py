import os
import time
import emoji as em
import speech_recognition as sr
import sys
from datetime import datetime
from nova_tts import read_aloud
from nova_weather import weather
from nova_whatsapp import send_msg
from nova_music import search_play, pause, resume
from nova_apps import open_app

# AI Fallback
try:
    from nova_genai import generate_response
except ImportError:
    def generate_response(prompt):
        return "Sorry, AI response feature is temporarily unavailable."

r = sr.Recognizer()
MIC_INDEX = None  # Customize if needed


def record_audio(timeout=7, phrase_time_limit=7):
    """Record audio and handle errors gracefully, returning recognized text or empty string."""
    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return r.recognize_google(audio)
    except sr.WaitTimeoutError:
        read_aloud("Listening timed out. Please try again.")
    except sr.UnknownValueError:
        read_aloud("I didn’t catch that. Please repeat.")
    except sr.RequestError:
        read_aloud("Network error. Please check your internet connection.")
    return ""  # return empty string instead of None for safety


def listen_for_command(timeout=7, phrase_time_limit=7):
    """Helper to get lowercased recognized speech or empty string."""
    text = record_audio(timeout, phrase_time_limit)
    if not text:
        return ""
    return text.lower()


def introduction():
    hour = datetime.now().hour
    if hour < 12:
        msg = "Good morning, happy soul."
    elif hour < 18:
        msg = "Good afternoon, happy soul."
    else:
        msg = "Good evening, happy soul."

    print("Nova:", msg)
    read_aloud(msg)
    time.sleep(0.5)
    read_aloud('Hello, I am Nova. Your personal voice assistant.')


def conversation_flow():
    read_aloud("Nova is waiting for you.")
    while True:
        start = listen_for_command()
        if not start:
            continue

        print("Heard:", start)
        if "nova" in start:
            introduction()
            while True:
                read_aloud("Speak to me, dearest.")
                prompt = listen_for_command()
                if not prompt:
                    continue

                print("You:", prompt)
                lower_prompt = prompt

                if any(x in lower_prompt for x in ["quit", "bye", "shut up", "exit"]):
                    print("Nova: " + em.emojize(":frowning_face:"))
                    read_aloud("Goodbye, happy soul.")
                    sys.exit(0)

                elif any(x in lower_prompt for x in ["capabilities", "abilities", "you do"]):
                    text = ("I can generate responses, forecast weather, send WhatsApp messages, "
                            "play music, and open apps for you.")
                    read_aloud(text)

                elif any(x in lower_prompt for x in ["hello", "hi", "hey"]):
                    read_aloud("Hey there good soul. I am Nova. I hope you have a nice day.")

                elif "who" in lower_prompt or "what" in lower_prompt:
                    reply = generate_response(prompt).replace("Gemini", "Nova").replace("Google", "Gemini")
                    read_aloud(reply)

                elif any(x in lower_prompt for x in ["open whatsapp", "open spotify", "open calculator", "open notepad", "open chrome"]):
                    for app in ["whatsapp", "spotify", "calculator", "notepad", "chrome"]:
                        if f"open {app}" in lower_prompt:
                            open_app(app)
                            break

                elif any(x in lower_prompt for x in ["music", "spotify", "song", "play music", "play song"]):
                    read_aloud("Connecting and opening Spotify.")
                    time.sleep(2)
                    search_play()

                    while True:
                        read_aloud("Say pause, resume, or disconnect.")
                        choose = listen_for_command(timeout=5, phrase_time_limit=5)
                        if not choose:
                            continue

                        if "pause" in choose:
                            pause()
                        elif "resume" in choose:
                            resume()
                        elif "disconnect" in choose:
                            read_aloud("Stop the song or keep it playing?")
                            confirm = listen_for_command(timeout=5, phrase_time_limit=5)
                            if not confirm or "stop" in confirm:
                                pause()
                            break

                elif "weather" in lower_prompt:
                    read_aloud("Tell me the city for the weather forecast.")
                    city = listen_for_command(timeout=5, phrase_time_limit=5)
                    if city:
                        weather(city)
                    else:
                        read_aloud("Sorry, I didn't catch the city name.")

                elif any(x in lower_prompt for x in ["whatsapp", "message"]):
                    read_aloud("Tell me the number to message.")
                    number = listen_for_command(timeout=5, phrase_time_limit=5)
                    if not number:
                        read_aloud("Sorry, I didn't get the number.")
                        continue
                    read_aloud("Tell me your message.")
                    message = listen_for_command(timeout=7, phrase_time_limit=7)
                    if not message:
                        read_aloud("Sorry, I didn't get the message.")
                        continue
                    send_msg(message, number)
                    read_aloud("I have sent your message.")

                else:
                    reply = generate_response(prompt)
                    read_aloud(reply)


if __name__ == '__main__':
    try:
        conversation_flow()
    except KeyboardInterrupt:
        print("\nExiting Nova. Goodbye, happy soul.")
        read_aloud("Goodbye, happy soul.")
        sys.exit(0)
