class CommandParser:
    def __init__(self):
        self.commands = {
            'ouvre': self._parse_open,
            'joue': self._parse_play,
            'heure': self._parse_time,
            'date': self._parse_date,
            'luminosité': self._parse_brightness,
            'volume': self._parse_volume
        }

    def parse_command(self, text):
        """Analyse le texte et retourne la commande et les arguments"""
        text = text.lower().strip()
        
        for cmd in self.commands:
            if text.startswith(cmd):
                return self.commands[cmd](text)
        
        return None, None

    def _parse_open(self, text):
        """Parse la commande 'ouvre'"""
        parts = text.split(maxsplit=1)
        if len(parts) > 1:
            return 'open', parts[1]
        return 'open', None

    def _parse_play(self, text):
        """Parse la commande 'joue'"""
        parts = text.split(maxsplit=1)
        if len(parts) > 1:
            return 'play', parts[1]
        return 'play', None

    def _parse_time(self, text):
        """Parse la commande 'heure'"""
        return 'time', None

    def _parse_date(self, text):
        """Parse la commande 'date'"""
        return 'date', None

    def _parse_brightness(self, text):
        """Parse la commande 'luminosité'"""
        parts = text.split()
        level = next((p for p in parts if p.isdigit() or p.endswith('%')), None)
        return 'brightness', level

    def _parse_volume(self, text):
        """Parse la commande 'volume'"""
        parts = text.split()
        level = next((p for p in parts if p.isdigit() or p.endswith('%')), None)
        return 'volume', level 