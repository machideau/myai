class VocalCalculator:
    def __init__(self):
        self.operations = {
            'plus': '+',
            'moins': '-',
            'fois': '*',
            'divisé par': '/',
            'pourcent': '%'
        }

    def calculate(self, expression):
        """Calcule une expression mathématique"""
        try:
            # Convertit l'expression vocale en expression mathématique
            for word, symbol in self.operations.items():
                expression = expression.replace(word, symbol)
            
            # Évalue l'expression
            result = eval(expression)
            return f"Le résultat est {result}"
        except Exception as e:
            return f"Erreur de calcul: {str(e)}"

    def convert_currency(self, amount, from_currency, to_currency):
        """Convertit une devise (à implémenter avec une API de taux de change)"""
        # À implémenter
        pass 