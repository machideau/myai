import os
import subprocess
import time
import json
from datetime import datetime, timedelta

class SystemManager:
    def __init__(self):
        self.shutdown_timer = None
        self.shortcuts_file = "shortcuts.json"
        self.shortcuts = self._load_shortcuts()

    def schedule_shutdown(self, minutes):
        """Programme l'arrêt de l'ordinateur"""
        if minutes > 0:
            shutdown_time = datetime.now() + timedelta(minutes=minutes)
            cmd = f'shutdown /s /t {minutes * 60}'
            subprocess.run(cmd, shell=True)
            return f"Arrêt programmé pour {shutdown_time.strftime('%H:%M')}"
        return "Durée invalide"

    def cancel_shutdown(self):
        """Annule l'arrêt programmé"""
        subprocess.run('shutdown /a', shell=True)
        return "Arrêt programmé annulé"

    def create_shortcut(self, name, command):
        """Crée un raccourci personnalisé"""
        self.shortcuts[name] = command
        self._save_shortcuts()
        return f"Raccourci '{name}' créé"

    def execute_shortcut(self, name):
        """Exécute un raccourci"""
        if name in self.shortcuts:
            try:
                subprocess.Popen(self.shortcuts[name], shell=True)
                return f"Exécution du raccourci '{name}'"
            except Exception as e:
                return f"Erreur: {str(e)}"
        return "Raccourci non trouvé"

    def _load_shortcuts(self):
        """Charge les raccourcis depuis le fichier"""
        try:
            with open(self.shortcuts_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_shortcuts(self):
        """Sauvegarde les raccourcis dans le fichier"""
        with open(self.shortcuts_file, 'w') as f:
            json.dump(self.shortcuts, f) 