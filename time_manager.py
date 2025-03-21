import threading
import time
from datetime import datetime, timedelta
import json

class TimeManager:
    def __init__(self):
        self.reminders = {}
        self.timers = {}
        self.reminders_file = "reminders.json"
        self._load_reminders()

    def set_reminder(self, message, time_str):
        """Crée un rappel"""
        try:
            reminder_time = datetime.strptime(time_str, "%H:%M")
            today = datetime.now()
            reminder_datetime = datetime.combine(today.date(), reminder_time.time())
            
            if reminder_datetime < datetime.now():
                reminder_datetime += timedelta(days=1)

            self.reminders[str(reminder_datetime)] = message
            self._save_reminders()
            
            # Démarre un thread pour le rappel
            threading.Thread(target=self._reminder_thread, 
                           args=(reminder_datetime, message)).start()
            
            return f"Rappel créé pour {time_str}"
        except ValueError:
            return "Format d'heure invalide"

    def set_timer(self, minutes, message):
        """Crée un minuteur"""
        timer_id = len(self.timers) + 1
        self.timers[timer_id] = {
            'end_time': datetime.now() + timedelta(minutes=minutes),
            'message': message
        }
        
        # Démarre un thread pour le minuteur
        threading.Thread(target=self._timer_thread, 
                        args=(timer_id, minutes, message)).start()
        
        return f"Minuteur de {minutes} minutes démarré"

    def _reminder_thread(self, reminder_time, message):
        """Thread pour gérer un rappel"""
        while datetime.now() < reminder_time:
            time.sleep(30)
        return f"RAPPEL: {message}"

    def _timer_thread(self, timer_id, minutes, message):
        """Thread pour gérer un minuteur"""
        time.sleep(minutes * 60)
        del self.timers[timer_id]
        return f"MINUTEUR TERMINÉ: {message}"

    def _load_reminders(self):
        """Charge les rappels depuis le fichier"""
        try:
            with open(self.reminders_file, 'r') as f:
                self.reminders = json.load(f)
        except:
            self.reminders = {}

    def _save_reminders(self):
        """Sauvegarde les rappels dans le fichier"""
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f) 