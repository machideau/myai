import os
import subprocess
import datetime
import webbrowser
import screen_brightness_control as sbc
import pycaw.pycaw as pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import winreg
import pywhatkit as kit
import pyautogui
import time
import speech_recognition as sr
import pyttsx3

class SystemCommands:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        # Initialize audio controller
        devices = pycaw.AudioUtilities.GetSpeakers()
        interface = devices.Activate(pycaw.IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_controller = cast(interface, POINTER(pycaw.IAudioEndpointVolume))
        self.whatsapp_window = None

    def _listen_for_response(self, prompt):
        """Écoute la réponse de l'utilisateur"""
        self.engine.say(prompt)
        self.engine.runAndWait()
        
        with sr.Microphone() as source:
            print(prompt)
            audio = self.recognizer.listen(source)
            try:
                response = self.recognizer.recognize_google(audio, language="fr-FR")
                print(f"Vous avez dit : {response}")
                return response.lower()
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None

    def find_executable_in_registry(self, app_name):
        """Cherche une application dans le registre Windows"""
        try:
            # Cherche dans les clés de registre communes pour les applications
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths")
            ]

            for hkey, path in registry_paths:
                try:
                    with winreg.OpenKey(hkey, f"{path}\\{app_name}.exe") as key:
                        return winreg.QueryValue(key, None)
                except WindowsError:
                    continue

                # Cherche dans les sous-clés
                try:
                    with winreg.OpenKey(hkey, path) as key:
                        i = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                if app_name.lower() in subkey_name.lower():
                                    with winreg.OpenKey(key, subkey_name) as subkey:
                                        return winreg.QueryValue(subkey, None)
                            except WindowsError:
                                break
                            i += 1
                except WindowsError:
                    continue

            return None
        except Exception:
            return None

    def find_executable_in_common_paths(self, app_name):
        """Cherche une application dans les dossiers communs"""
        common_paths = [
            os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
            os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
            os.environ.get('LOCALAPPDATA', ''),
            os.environ.get('APPDATA', ''),
            r'C:\Windows',
            r'C:\Windows\System32'
        ]

        # Différentes extensions possibles pour les exécutables
        extensions = ['.exe', '.msi', '.bat', '.cmd']
        
        for path in common_paths:
            if not path or not os.path.exists(path):
                continue
                
            # Parcours récursif des dossiers
            for root, _, files in os.walk(path):
                for file in files:
                    if any(file.lower() == f"{app_name.lower()}{ext}" for ext in extensions):
                        return os.path.join(root, file)
                    elif app_name.lower() in file.lower() and any(file.endswith(ext) for ext in extensions):
                        return os.path.join(root, file)
        return None

    def find_uwp_app(self, app_name):
        """Cherche une application Windows Store (UWP)"""
        try:
            # Cherche dans le registre pour les applications UWP
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                              r"Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages") as key:
                i = 0
                while True:
                    try:
                        package_name = winreg.EnumKey(key, i)
                        if app_name.lower() in package_name.lower():
                            # Construit la commande shell:appsfolder
                            app_id = f"shell:appsFolder\\{package_name}!App"
                            return app_id
                    except WindowsError:
                        break
                    i += 1
            return None
        except Exception:
            return None

    def find_whatsapp(self):
        """Cherche spécifiquement l'application WhatsApp installée"""
        # Essayer d'abord la commande UWP directe
        uwp_command = "explorer.exe shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
        try:
            subprocess.Popen(uwp_command)
            return uwp_command
        except:
            pass

        # Chercher dans les chemins possibles
        possible_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'WhatsApp', 'WhatsApp.exe'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'WhatsApp', 'WhatsApp.exe'),
            r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_*\WhatsApp.exe",
            r"C:\Program Files (x86)\WhatsApp\WhatsApp.exe",
        ]
        
        # Chercher dans les chemins spécifiques
        for path in possible_paths:
            if '*' in path:  # Pour les chemins avec wildcard
                import glob
                matches = glob.glob(path)
                if matches:
                    return matches[0]
            elif os.path.exists(path):
                return path

        # Chercher dans le registre
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\WhatsApp.exe")
            path = winreg.QueryValue(key, None)
            if os.path.exists(path):
                return path
        except:
            pass

        return None  # Ne plus retourner "web" comme fallback

    def open_application(self, app_name):
        """Ouvre une application"""
        # Normalisation du nom de l'application
        app_name = app_name.lower().strip()
        
        # Applications spéciales avec leurs commandes ou chemins
        special_apps = {
            "whatsapp": {
                "installed": self.find_whatsapp,  # Fonction qui cherche WhatsApp installé
                "cmd": "start whatsapp:",         # Protocole WhatsApp
                "alt_cmd": "explorer.exe shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"  # Commande UWP
            },
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
            # Gestion spéciale pour WhatsApp et autres apps similaires
            if app_name in special_apps:
                if isinstance(special_apps[app_name], dict):
                    # Pour WhatsApp, essaie d'abord de trouver l'application installée
                    if "installed" in special_apps[app_name]:
                        whatsapp_path = special_apps[app_name]["installed"]()
                        if whatsapp_path:
                            subprocess.Popen(whatsapp_path)
                            return f"J'ouvre {app_name}"
                    
                    # Essaie ensuite les autres méthodes
                    for cmd_type, cmd in special_apps[app_name].items():
                        if cmd_type != "installed":  # Skip la méthode "installed" déjà essayée
                            try:
                                if cmd_type == "cmd":
                                    os.system(cmd)
                                    return f"J'ouvre {app_name}"
                                elif cmd_type == "alt_cmd":
                                    subprocess.Popen(["explorer.exe", cmd])
                                    return f"J'ouvre {app_name}"
                            except:
                                continue
                else:
                    subprocess.Popen(special_apps[app_name])
                    return f"J'ouvre {app_name}"
            
            # Cherche dans le registre
            exe_path = self.find_executable_in_registry(app_name)
            if exe_path and os.path.exists(exe_path):
                subprocess.Popen(exe_path)
                return f"J'ouvre {app_name}"
            
            # Cherche les applications UWP
            uwp_app = self.find_uwp_app(app_name)
            if uwp_app:
                subprocess.Popen(["explorer.exe", uwp_app])
                return f"J'ouvre {app_name}"
            
            # Cherche dans les dossiers communs
            exe_path = self.find_executable_in_common_paths(app_name)
            if exe_path:
                subprocess.Popen(exe_path)
                return f"J'ouvre {app_name}"
            
            return f"Je ne trouve pas l'application {app_name}"
        except Exception as e:
            return f"Erreur lors de l'ouverture de {app_name}: {str(e)}"

    def _is_app_running(self, app_name):
        """Vérifie si une application est déjà en cours d'exécution"""
        try:
            output = subprocess.check_output('tasklist', shell=True).decode()
            return app_name.lower() in output.lower()
        except:
            return False

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

    def send_whatsapp_message(self, *args):
        """Envoie un message WhatsApp de manière interactive"""
        try:
            # Demande le nom du contact avec possibilité de réessayer
            max_attempts = 3
            attempt = 0
            contact = None
            
            while attempt < max_attempts and not contact:
                contact = self._listen_for_response("À qui voulez-vous envoyer un message ?")
                if not contact:
                    retry = self._listen_for_response("Je n'ai pas compris. Voulez-vous réessayer ?")
                    if not retry or 'non' in retry.lower():
                        return "Envoi du message annulé"
                    attempt += 1
            
            if not contact:
                return "Désolé, je n'ai pas réussi à comprendre le nom du contact"

            # Demande le message
            message = self._listen_for_response("Quel message voulez-vous envoyer ?")
            if not message:
                return "Je n'ai pas compris le message"

            # Vérifie WhatsApp
            whatsapp_path = self.find_whatsapp()
            if not whatsapp_path:
                return "WhatsApp n'est pas installé ou n'a pas été trouvé"

            # Lance WhatsApp s'il n'est pas déjà en cours d'exécution
            if not self._is_app_running('WhatsApp.exe'):
                try:
                    subprocess.Popen(whatsapp_path)
                    time.sleep(5)  # Attendre que WhatsApp soit bien lancé
                except Exception as e:
                    return f"Erreur lors du lancement de WhatsApp: {str(e)}"

            # Mettre le focus sur la fenêtre WhatsApp
            try:
                # Attendre que la fenêtre soit active
                pyautogui.getWindowsWithTitle("WhatsApp")[0].activate()
                time.sleep(1)
            except:
                return "Impossible de trouver la fenêtre WhatsApp"

            try:
                # Recherche le contact
                pyautogui.hotkey('ctrl', 'f')  # Ouvre la recherche
                time.sleep(1.5)
                pyautogui.write(contact)
                time.sleep(2)  # Attendre que la recherche s'effectue
                
                # Sélectionner le premier résultat
                pyautogui.press('enter')
                time.sleep(2)  # Attendre que la conversation s'ouvre
                
                # Vérifier si on est dans la zone de message
                pyautogui.press('tab')  # Pour s'assurer d'être dans la zone de message
                time.sleep(0.5)
                
                # Écrire et envoyer le message
                pyautogui.write(message)
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(0.5)

                return f"Message envoyé à {contact}"
            except Exception as e:
                return f"Erreur lors de l'envoi du message: {str(e)}"
            
        except Exception as e:
            return f"Erreur lors de l'envoi du message: {str(e)}"

    def start_whatsapp_call(self, _, video=False):
        """Démarre un appel WhatsApp de manière interactive"""
        try:
            # Demande le nom du contact
            prompt = "Qui voulez-vous appeler ?" if not video else "Avec qui voulez-vous démarrer un appel vidéo ?"
            contact = self._listen_for_response(prompt)
            if not contact:
                return "Je n'ai pas compris le nom du contact"

            # Ouvre WhatsApp
            whatsapp_path = self.find_whatsapp()
            if not whatsapp_path:
                return "WhatsApp n'est pas installé"

            if not self._is_app_running('WhatsApp.exe'):
                subprocess.Popen(whatsapp_path)
                time.sleep(3)

            # Ouvre la conversation
            kit.open_web()
            time.sleep(2)
            pyautogui.write(contact)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(2)

            # Clique sur le bouton d'appel approprié
            if video:
                # Coordonnées du bouton d'appel vidéo
                pyautogui.click(x=1200, y=60)
            else:
                # Coordonnées du bouton d'appel audio
                pyautogui.click(x=1150, y=60)

            return f"Appel {'vidéo ' if video else ''}WhatsApp vers {contact}"
        except Exception as e:
            return f"Erreur lors de l'appel: {str(e)}" 
