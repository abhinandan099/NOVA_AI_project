import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate

def read_aloud(text):
    engine.say(text)
    engine.runAndWait()



'''
import pyttsx3

engine = pyttsx3.init()

def read_aloud(text):
    engine.say(text)
    engine.runAndWait()
'''