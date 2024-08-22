import customtkinter as ctk
from mus.util import PlayerState, EVENT_INTERVAL


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
        self.song_length = song_length
        self.update_progress_bar()

    def update_progress_bar(self):
        if self.music_player.STATE == PlayerState.PLAYING:
            song_position = self.music_player.get_song_position()

            # GETS RATIO OF PROGRESS
            progress = song_position / self.song_length
            self.progress_bar.set(progress)
            minutes = int(song_position // 60)
            seconds = int(song_position % 60)
            time_string = f"{minutes:02d}:{seconds:02d}"

            self.music_player.control_bar.playback_label.configure(text=time_string)

            if song_position < self.song_length:
                self.after(EVENT_INTERVAL, self.update_progress_bar)

            self.music_player.check_for_events()

        elif self.music_player.STATE == PlayerState.PAUSED:
            self.after(EVENT_INTERVAL, self.update_progress_bar)
        else:
            self.progress_bar.set(0)
