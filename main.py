import speech_recognition as sr
import pyttsx3
from rich.console import Console
from rich.status import Status
from system_commands import SystemCommands
from command_parser import CommandParser
from music_commands import MusicPlayer
from system_manager import SystemManager
from time_manager import TimeManager
from note_manager import NoteManager
from translator import TranslationManager
from calculator import VocalCalculator
import translator

def initialize_voice():
    engine = pyttsx3.init()
    # Configuration de la voix (optionnel)
    engine.setProperty('rate', 150)    # Vitesse de parole
    engine.setProperty('volume', 0.9)  # Volume (0 à 1)
    return engine

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Je vous écoute...")
        audio = recognizer.listen(source)
    return audio

def execute_command(command, arg, system_commands, music_player, system_manager, time_manager, note_manager, translator, calculator):
    """Exécute la commande système appropriée"""
    if command == 'open':
        return system_commands.open_application(arg)
    elif command == 'play':
        return system_commands.play_youtube(arg)
    elif command == 'time':
        return system_commands.get_time()
    elif command == 'date':
        return system_commands.get_date()
    elif command == 'brightness':
        return system_commands.set_brightness(arg)
    elif command == 'volume':
        return system_commands.set_volume(arg)
    elif command == 'music':
        return music_player.play_music(arg)
    elif command == 'pause':
        return music_player.pause_resume()
    elif command == 'shutdown':
        return system_manager.schedule_shutdown(int(arg))
    elif command == 'reminder':
        return time_manager.set_reminder(arg['message'], arg['time'])
    elif command == 'timer':
        return time_manager.set_timer(int(arg['minutes']), arg['message'])
    elif command == 'note':
        return note_manager.create_note(arg)
    elif command == 'list':
        return note_manager.add_to_list(arg)
    elif command == 'translate':
        return translator.translate_text(arg['text'], arg['language'])
    elif command == 'calculate':
        return calculator.calculate(arg)
    elif command == 'whatsapp_message':
        return system_commands.send_whatsapp_message()
    elif command == 'whatsapp_call':
        return system_commands.start_whatsapp_call(None)
    elif command == 'whatsapp_video':
        return system_commands.start_whatsapp_call(None, video=True)
    return "Commande non prédéfinie"

def main():
    console = Console()
    engine = initialize_voice()
    recognizer = sr.Recognizer()
    system_commands = SystemCommands()
    command_parser = CommandParser()

    # Initialize new managers
    music_player = MusicPlayer()
    system_manager = SystemManager()
    time_manager = TimeManager()
    note_manager = NoteManager()
    translator = TranslationManager()
    calculator = VocalCalculator()

    console.print("[bold green]Assistant vocal démarré![/]")
    console.print("[bold blue]Commandes disponibles:[/]")
    console.print("- 'ouvre [application]' : ouvre une application")
    console.print("- 'joue [titre]' : recherche et joue sur YouTube")
    console.print("- 'heure' : donne l'heure actuelle")
    console.print("- 'date' : donne la date actuelle")
    console.print("- 'luminosité [0-100]' : règle la luminosité")
    console.print("- 'volume [0-100]' : règle le volume")
    console.print("- 'joue musique [titre]' : joue de la musique locale")
    console.print("- 'pause' : met en pause/reprend la musique")
    console.print("- 'éteins dans [minutes]' : programme l'arrêt")
    console.print("- 'rappelle-moi [message] à [heure]' : crée un rappel")
    console.print("- 'minuteur [minutes] [message]' : crée un minuteur")
    console.print("- 'note [texte]' : crée une note")
    console.print("- 'liste [item]' : ajoute à la liste de courses")
    console.print("- 'traduis [texte] en [langue]' : traduit un texte")
    console.print("- 'calcule [expression]' : effectue un calcul")
    console.print("- 'message' : envoyer un message WhatsApp")
    console.print("- 'appel' : faire un appel audio WhatsApp")
    console.print("- 'video' : faire un appel vidéo WhatsApp")
    console.print("- 'au revoir' : quitte l'assistant")

    while True:
        try:
            with console.status("[bold green]En attente de votre commande...") as status:
                audio = listen()
                
            with console.status("[bold yellow]Traitement de votre commande..."):
                try:
                    text = recognizer.recognize_google(audio, language="fr-FR")
                    console.print(f"[bold blue]Vous avez dit:[/] {text}")

                    if "au revoir" in text.lower():
                        response = "Au revoir! À bientôt!"
                        console.print(f"[bold green]Réponse:[/] {response}")
                        engine.say(response)
                        engine.runAndWait()
                        break

                    command, arg = command_parser.parse_command(text)
                    if command:
                        response = execute_command(command, arg, system_commands, music_player, system_manager, time_manager, note_manager, translator, calculator)
                    else:
                        response = "Je ne comprends pas cette commande"

                    console.print(f"[bold green]Réponse:[/] {response}")
                    engine.say(response)
                    engine.runAndWait()

                except sr.UnknownValueError:
                    console.print("[bold red]Désolé, je n'ai pas compris.[/]")
                except sr.RequestError:
                    console.print("[bold red]Erreur de service. Vérifiez votre connexion internet.[/]")

        except KeyboardInterrupt:
            console.print("\n[bold red]Programme arrêté par l'utilisateur.[/]")
            break

if __name__ == "__main__":
    main()


