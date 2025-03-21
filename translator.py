from googletrans import Translator

class TranslationManager:
    def __init__(self):
        self.translator = Translator()
        self.language_codes = {
            'français': 'fr',
            'anglais': 'en',
            'espagnol': 'es',
            'allemand': 'de',
            'italien': 'it',
            'portugais': 'pt'
        }

    def translate_text(self, text, target_lang):
        """Traduit un texte vers la langue cible"""
        try:
            if target_lang.lower() in self.language_codes:
                target_code = self.language_codes[target_lang.lower()]
                result = self.translator.translate(text, dest=target_code)
                return f"Traduction: {result.text}"
            return "Langue non supportée"
        except Exception as e:
            return f"Erreur de traduction: {str(e)}" 