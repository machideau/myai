import os
from pathlib import Path
import win32com.client

class MusicPlayer:
    def __init__(self):
        self.player = win32com.client.Dispatch("WMPlayer.OCX")
        self.music_dir = str(Path.home() / "Music")
        self.current_playlist = []
        self.is_playing = False

    def play_music(self, query):
        """Joue de la musique depuis le dossier musical"""
        music_files = self._find_music_files(query)
        if music_files:
            self.current_playlist = music_files
            self._play_file(music_files[0])
            return f"Je joue {os.path.basename(music_files[0])}"
        return "Aucune musique trouvée"

    def pause_resume(self):
        """Met en pause ou reprend la lecture"""
        if self.is_playing:
            self.player.controls.pause()
            self.is_playing = False
            return "Musique en pause"
        else:
            self.player.controls.play()
            self.is_playing = True
            return "Reprise de la lecture"

    def _find_music_files(self, query):
        """Recherche des fichiers musicaux correspondant à la requête"""
        music_files = []
        for root, _, files in os.walk(self.music_dir):
            for file in files:
                if file.lower().endswith(('.mp3', '.wav', '.flac', '.wma')) and query.lower() in file.lower():
                    music_files.append(os.path.join(root, file))
        return music_files

    def _play_file(self, file_path):
        """Joue un fichier musical"""
        media = self.player.newMedia(file_path)
        self.player.currentPlaylist.appendItem(media)
        self.player.controls.play()
        self.is_playing = True 