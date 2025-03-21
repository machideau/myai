# Assistant Vocal Python

Un assistant vocal en Python capable d'exécuter diverses commandes système via la reconnaissance vocale.

## Fonctionnalités

### Commandes de Base
- Reconnaissance vocale en français
- Synthèse vocale pour les réponses
- Ouverture d'applications
- Lecture de vidéos YouTube
- Affichage de l'heure et de la date
- Contrôle de la luminosité de l'écran
- Réglage du volume système

### Gestion de la Musique
- Lecture de musique locale
- Contrôle de lecture (pause/reprise)
- Gestion de playlists

### Gestion du Système
- Arrêt programmé de l'ordinateur
- Création et exécution de raccourcis personnalisés

### Gestion du Temps
- Création de rappels avec message et heure
- Minuteurs personnalisables
- Gestion des alarmes

### Prise de Notes
- Création de notes vocales
- Gestion de listes (courses, tâches, etc.)
- Organisation par catégories

### Traduction
- Traduction instantanée entre plusieurs langues
- Support des langues principales (français, anglais, espagnol, etc.)

### Calculatrice Vocale
- Calculs mathématiques simples
- Conversions d'unités
- Calculs de pourcentages

## Commandes Disponibles

- `ouvre [application]` : Ouvre une application
- `joue [titre]` : Recherche et joue sur YouTube
- `heure` : Donne l'heure actuelle
- `date` : Donne la date actuelle
- `luminosité [0-100]` : Règle la luminosité
- `volume [0-100]` : Règle le volume
- `joue musique [titre]` : Joue de la musique locale
- `pause` : Met en pause/reprend la musique
- `éteins dans [minutes]` : Programme l'arrêt
- `rappelle-moi [message] à [heure]` : Crée un rappel
- `minuteur [minutes] [message]` : Crée un minuteur
- `note [texte]` : Crée une note
- `liste [item]` : Ajoute à la liste de courses
- `traduis [texte] en [langue]` : Traduit un texte
- `calcule [expression]` : Effectue un calcul
- `au revoir` : Quitte l'assistant

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

## Dépendances Principales

- SpeechRecognition : Reconnaissance vocale
- pyttsx3 : Synthèse vocale
- rich : Interface console améliorée
- python-vlc : Lecture de musique
- googletrans : Traduction
- screen-brightness-control : Contrôle de la luminosité
- pycaw : Contrôle du volume système

## Structure du Projet

- `voice_chat.py` : Script principal de l'assistant
- `system_commands.py` : Gestionnaire des commandes système
- `command_parser.py` : Analyseur des commandes vocales
- `music_commands.py` : Gestionnaire de musique
- `system_manager.py` : Gestionnaire système avancé
- `time_manager.py` : Gestionnaire de temps
- `note_manager.py` : Gestionnaire de notes
- `translator.py` : Gestionnaire de traduction
- `calculator.py` : Calculatrice vocale

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## Licence

MIT License

## Auteur

[SAM le DEV](https://samledev.onrender.com/)
