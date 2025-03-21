# Assistant Vocal Python

Un assistant vocal en Python capable d'exécuter diverses commandes système via la reconnaissance vocale.

## Fonctionnalités

- Reconnaissance vocale en français
- Synthèse vocale pour les réponses
- Commandes système :
  - Ouverture d'applications
  - Lecture de vidéos YouTube
  - Affichage de l'heure et de la date
  - Contrôle de la luminosité de l'écran
  - Réglage du volume système

## Prérequis

- Python 3.7+
- Un microphone fonctionnel
- Une connexion Internet (pour la reconnaissance vocale)

## Installation

1. Clonez le repository :
```bash
git clone https://github.com/machideau/myai.git
cd assistant-vocal
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

Lancez l'assistant avec :
```bash
python voice_chat.py
```

### Commandes disponibles

- `ouvre [application]` : Ouvre une application (ex: chrome, notepad, calculatrice)
- `joue [titre]` : Recherche et joue une vidéo sur YouTube
- `heure` : Donne l'heure actuelle
- `date` : Donne la date actuelle
- `luminosité [0-100]` : Règle la luminosité de l'écran
- `volume [0-100]` : Règle le volume système
- `au revoir` : Quitte l'assistant

## Structure du projet

- `voice_chat.py` : Script principal de l'assistant
- `system_commands.py` : Gestionnaire des commandes système
- `command_parser.py` : Analyseur des commandes vocales
- `requirements.txt` : Liste des dépendances

## Dépendances principales

- SpeechRecognition : Reconnaissance vocale
- pyttsx3 : Synthèse vocale
- rich : Interface console améliorée
- screen-brightness-control : Contrôle de la luminosité
- pycaw : Contrôle du volume système

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## Licence

MIT License

## Auteur

[SAM le DEV](https://samledev.onrender.com)
