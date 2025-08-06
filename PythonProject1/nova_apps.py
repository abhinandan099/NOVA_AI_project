import os
import subprocess


def open_app(app_name):
    app_paths = {
        "whatsapp": r"C:\Users\HP\Desktop\WhatsApp - Shortcut.lnk",
        "spotify": r"C:\Users\HP\Desktop\Spotify - Shortcut.lnk",
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        # Add more apps and their paths here if needed
    }

    app_name = app_name.lower()
    if app_name not in app_paths:
        print(f"App '{app_name}' not found in path list.")
        return

    path = app_paths[app_name]

    try:
        # If path is absolute, check if file exists
        if os.path.isabs(path):
            if not os.path.exists(path):
                print(f"File not found: {path}")
                return
            # Use os.startfile for .exe or .lnk files (Windows)
            if path.lower().endswith(('.exe', '.lnk')):
                os.startfile(path)
            else:
                # For other file types or folders, use subprocess
                subprocess.Popen([path])
        else:
            # If path is a command like 'calc.exe' or 'notepad.exe'
            subprocess.Popen([path])
    except Exception as e:
        print(f"Failed to open {app_name}: {e}")
