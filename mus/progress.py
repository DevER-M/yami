import customtkinter as ctk


class BottomFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # SETUP
        self.music_player = parent

        self.progress_bar = ctk.CTkProgressBar(self, progress_color="#1f0469")
        self.progress_bar.pack(fill="x", expand=True)
        self.progress_bar.set(0)

        self.pack(fill="x")  # IMP

    def start_progress_bar(self, song_length):
        self.progress_bar.set(0)
        self.music_player.song_length = song_length
        self.music_player.update()
