import os
from datetime import datetime

class NoteManager:
    def __init__(self):
        self.notes_dir = "notes"
        self._ensure_notes_dir()

    def create_note(self, content, category="general"):
        """Crée une nouvelle note"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.notes_dir}/{category}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Note créée dans {filename}"

    def add_to_list(self, item, list_name="courses"):
        """Ajoute un élément à une liste"""
        filename = f"{self.notes_dir}/{list_name}.txt"
        
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"- {item}\n")
        
        return f"'{item}' ajouté à la liste {list_name}"

    def read_list(self, list_name="courses"):
        """Lit une liste"""
        filename = f"{self.notes_dir}/{list_name}.txt"
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return content if content else "Liste vide"
        except FileNotFoundError:
            return "Liste non trouvée"

    def _ensure_notes_dir(self):
        """Crée le dossier des notes s'il n'existe pas"""
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir) 