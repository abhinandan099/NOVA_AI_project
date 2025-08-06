'''import spotipy
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr
from nova_tts import read_aloud
import sounddevice as sd
import numpy as np

client_id = 'your-client-id'
client_secret = 'your-client-secret'
redirect_uri = 'your-redirect-uri'

scope = ['user-read-playback-state', 'user-modify-playback-state']

sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=sp_oauth)

r = sr.Recognizer()
fs = 44100  # sample rate

def record_audio(duration=5):
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    audio = np.squeeze(audio)
    audio_int16 = (audio * 32767).astype(np.int16)
    return sr.AudioData(audio_int16.tobytes(), fs, 2)

def search_play():
    read_aloud("Tell me the name of the song you want to search for")
    audio = record_audio(duration=5)
    song = r.recognize_google(audio)
    results = sp.search(q=song, limit=1, type='track')
    print("You said:", song)
    for i, t in enumerate(results['tracks']['items']):
        print(f"{i + 1}. {t['name']} - {t['artists'][0]['name']}")
    read_aloud("Are you sure?")
    audio = record_audio(duration=4)
    choice = r.recognize_google(audio)
    if "yes" in choice.lower():
        track_id = results['tracks']['items'][0]['id']
        sp.start_playback(uris=['spotify:track:' + track_id])
        track = sp.track(track_id)
        name = track['name']
        artist = track['artists'][0]['name']
        read_aloud(f"Playing {name} by {artist}")
    else:
        read_aloud("Better luck next time, dear")

def pause():
    sp.pause_playback()
    read_aloud("Song paused")

def resume():
    sp.start_playback()
    read_aloud("Song resumed")
'''


import spotipy
from spotipy.oauth2 import SpotifyOAuth
from nova_tts import read_aloud
import speech_recognition as sr
import time
import signal
import sys

# Replace with your actual Spotify credentials
client_id = 'your-client-id'
client_secret = 'your-client-secret'
redirect_uri = 'http://127.0.0.1:8888/callback'  # Use loopback IP instead of localhost

scope = ['user-read-playback-state', 'user-modify-playback-state']

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    print("\nExecution interrupted. Exiting gracefully...")
    read_aloud("Goodbye, happy soul.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Spotify authorization with timeout (example 60 seconds)
def get_spotify_client(timeout=60):
    import threading

    sp_client = [None]
    exc = [None]

    def auth():
        try:
            sp_client[0] = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope
            ))
        except Exception as e:
            exc[0] = e

    thread = threading.Thread(target=auth)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        read_aloud("Spotify authorization timed out. Please try again later.")
        sys.exit(1)
    if exc[0]:
        print(f"Spotify auth error: {exc[0]}")
        read_aloud("Error during Spotify authorization.")
        sys.exit(1)
    return sp_client[0]

sp = get_spotify_client()
r = sr.Recognizer()

def ensure_active_device():
    """Try to transfer playback to an active device if not already set."""
    devices = sp.devices().get('devices', [])
    if not devices:
        read_aloud("No active Spotify device found. Please open Spotify on your phone or computer.")
        return False
    active_device = next((d for d in devices if d['is_active']), None)
    if not active_device:
        device_id = devices[0]['id']
        sp.transfer_playback(device_id=device_id, force_play=True)
        time.sleep(1)
    return True

def search_play():
    read_aloud("Tell me the name of the song you want to play.")
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening for song name...")
            audio = r.listen(source, timeout=7, phrase_time_limit=7)
        song = r.recognize_google(audio)
    except Exception as e:
        print(f"Error recognizing song: {e}")
        read_aloud("Sorry, I couldn't get the song name.")
        return

    print("You said:", song)
    results = sp.search(q=song, limit=1, type='track')
    if not results['tracks']['items']:
        read_aloud("Sorry, I couldn't find the song.")
        return

    track_info = results['tracks']['items'][0]
    song_name = track_info['name']
    artist_name = track_info['artists'][0]['name']

    read_aloud(f"Do you want to play {song_name} by {artist_name}? Say yes or no.")
    try:
        with sr.Microphone() as source:
            print("Listening for confirmation...")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        choice = r.recognize_google(audio).lower()
    except Exception as e:
        print("Confirmation failed:", e)
        read_aloud("I didn't catch that. Cancelling playback.")
        return

    if "yes" in choice:
        if ensure_active_device():
            sp.start_playback(uris=['spotify:track:' + track_info['id']])
            read_aloud(f"Playing {song_name} by {artist_name}")
    else:
        read_aloud("Okay, maybe next time.")

def pause():
    try:
        sp.pause_playback()
        read_aloud("Song paused.")
    except Exception as e:
        print("Pause error:", e)
        read_aloud("Unable to pause music.")

def resume():
    try:
        if ensure_active_device():
            sp.start_playback()
            read_aloud("Song resumed.")
    except Exception as e:
        print("Resume error:", e)
        read_aloud("Unable to resume music.")
