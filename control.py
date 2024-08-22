import customtkinter as ctk
from util import BUTTON_WIDTH,PlayerState
import tkinter as tk


class ControlBar(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        pause_icon,
        play_icon,
        prev_icon,
        next_icon,
        play_next_command,
    ):
        super().__init__(parent, corner_radius=10, fg_color="#121212")

        # SETUP
        self.music_player = parent
        self.pause_icon = pause_icon
        self.play_icon = play_icon
        self.play_next_command = play_next_command
        self.title_max_chars = 40

        # WIDGETS
        self.play_button = ctk.CTkButton(
            self,
            command=self.play_pause,
            width=BUTTON_WIDTH,
            height=10,
            text="",
            image=pause_icon,
            corner_radius=10,
        )
        self.next_button = ctk.CTkButton(
            self,
            command=play_next_command,
            width=BUTTON_WIDTH,
            text="",
            corner_radius=10,
            image=next_icon,
        )
        self.prev_button = ctk.CTkButton(
            self,
            text="",
            width=BUTTON_WIDTH,
            corner_radius=10,
            command=self.play_previous,
            image=prev_icon,
        )
        self.music_title_label = ctk.CTkLabel(
            self,
            text="",
            font=("roboto", 12),
            fg_color="#121212",
            width=20,
            anchor="w",
        )
        self.playback_label = ctk.CTkLabel(
            self, text="0:00", font=("roboto", 12), fg_color="#121212"
        )

        # PLACEMENT
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)

        # PLACEMENT
        self.music_title_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)
        self.playback_label.grid(row=0, column=1, sticky="w", padx=5, pady=10)
        self.prev_button.grid(row=0, column=2, sticky="nsew", padx=5, pady=10)
        self.play_button.grid(row=0, column=3, sticky="nsew", padx=5, pady=10)
        self.next_button.grid(row=0, column=4, sticky="nsew", padx=5, pady=10)

    def play_pause(self, event=None):
        if self.music_player.STATE == PlayerState.PLAYING:
            self.music_player.music.pause()
            self.music_player.STATE = PlayerState.PAUSED
        else:
            self.music_player.music.unpause()
            self.music_player.STATE = PlayerState.PLAYING
        self.update_play_button(self.music_player.state)

    def update_play_button(self, state):
        if state == PlayerState.PLAYING:
            self.play_button.configure(image=self.pause_icon)
        else:
            self.play_button.configure(image=self.play_icon)

    def play_previous(self, event=None):
        if not self.music_player.playlist:
            return

        # PLAY FROM END
        elif self.music_player.playlist_index == 0:
            self.music_player.playlist_index = len(self.music_player.playlist) - 1
        # PLAY PREVIOUS
        else:
            self.music_player.playlist_index -= 1
        self.music_player.load_and_play_song(self.music_player.playlist_index)

        # UPDATE SELECTION
        self.music_player.playlist_frame.song_list.selection_clear(0, tk.END)
        self.music_player.playlist_frame.song_list.select_set(
            self.music_player.playlist_index
        )

    # TRUNCATOR
    def set_music_title(self, title):
        if len(title) > self.title_max_chars:
            truncated_title = title[: self.title_max_chars - 3] + "..."
        else:
            truncated_title = title
        self.music_title_label.configure(text=truncated_title)