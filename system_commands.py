import os
import subprocess
import datetime
import webbrowser
import screen_brightness_control as sbc
import pycaw.pycaw as pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class SystemCommands:
    def __init__(self):
        # Initialize audio controller
        devices = pycaw.AudioUtilities.GetSpeakers()
        interface = devices.Activate(pycaw.IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_controller = cast(interface, POINTER(pycaw.IAudioEndpointVolume))

    def open_application(self, app_name):
        """Ouvre une application"""
        # Normalisation du nom de l'application
        app_name = app_name.lower().strip()
        
        common_paths = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "bloc-note": "notepad.exe",
            "bloc-notes": "notepad.exe",
            "notepad": "notepad.exe",
            "calculatrice": "calc.exe",
            "calculette": "calc.exe",
            "explorateur": "explorer.exe"
        }
        
        try:
            if app_name in common_paths:
                subprocess.Popen(common_paths[app_name])
                return f"J'ouvre {app_name}"
            else:
                return f"Je ne connais pas l'application {app_name}"
        except Exception as e:
            return f"Erreur lors de l'ouverture de {app_name}: {str(e)}"

    def play_youtube(self, query):
        """Recherche et joue une vidéo sur YouTube"""
        search_query = query.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(url)
        return f"Je recherche {query} sur YouTube"

    def get_time(self):
        """Donne l'heure actuelle"""
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"Il est {current_time}"

    def get_date(self):
        """Donne la date actuelle"""
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        return f"Nous sommes le {current_date}"

    def set_brightness(self, level):
        """Règle la luminosité de l'écran"""
        try:
            if isinstance(level, str):
                if level.endswith("%"):
                    level = int(level[:-1])
                else:
                    level = int(level)
            
            level = max(0, min(100, level))
            sbc.set_brightness(level)
            return f"Luminosité réglée à {level}%"
        except Exception as e:
            return f"Erreur lors du réglage de la luminosité: {str(e)}"

    def set_volume(self, level):
        """Règle le volume système"""
        try:
            if isinstance(level, str):
                if level.endswith("%"):
                    level = int(level[:-1])
                else:
                    level = int(level)
            
            level = max(0, min(100, level))
            volume_scalar = level / 100.0
            self.volume_controller.SetMasterVolumeLevelScalar(volume_scalar, None)
            return f"Volume réglé à {level}%"
        except Exception as e:
            return f"Erreur lors du réglage du volume: {str(e)}" 