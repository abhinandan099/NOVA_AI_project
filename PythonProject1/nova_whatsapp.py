import pywhatkit
import pyautogui
import time
from nova_tts import read_aloud
from datetime import datetime


def send_msg(msg, person):
    now = datetime.now()
    hour = now.hour
    minute = now.minute + 1

    # Handle minute overflow and hour increment
    if minute >= 60:
        minute %= 60
        hour = (hour + 1) % 24

    try:
        # Customize the country code as needed, e.g., '+91' for India
        full_number = '+91' + person.strip()  # strip to avoid extra spaces
        read_aloud(f"Sending message to {full_number} shortly.")

        # Send the WhatsApp message scheduled 1 minute from now
        pywhatkit.sendwhatmsg(full_number, msg, hour, minute, wait_time=10, tab_close=True, close_time=3)

        # Wait for WhatsApp web to open and send the message
        time.sleep(10)

        # Press Enter to send the message if not already sent
        pyautogui.press('enter')

        # Wait a bit and then close the tab safely
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'w')  # Close the current tab

        read_aloud("Message sent successfully.")
    except Exception as e:
        print("Error sending WhatsApp message:", e)
        read_aloud("Sorry, there was an error sending your message.")


'''
import pywhatkit
import pyautogui
import time
from datetime import datetime
from nova_tts import read_aloud

def send_msg(msg, person):
    now = datetime.now()
    hour = now.hour
    minute = now.minute + 1

    if minute >= 60:
        minute = minute % 60
        hour = (hour + 1) % 24

    try:
        full_number = '+91' + person  # You can make this dynamic later
        pywhatkit.sendwhatmsg(full_number, msg, hour, minute, wait_time=10)
        time.sleep(10)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'w')
        pyautogui.hotkey('ctrl', 'shift', 'w')
        read_aloud("Message sent successfully.")
    except Exception as e:
        error = "Error while sending message."
        print("Nova:", error)
        print("Details:", e)
        read_aloud(error)
'''