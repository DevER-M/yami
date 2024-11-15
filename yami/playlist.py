"""Playlist"""

import tkinter as tk
import customtkinter as ctk


class PlaylistFrame(ctk.CTkFrame):
    """Playlist Holder"""

    def __init__(self, parent):
        super().__init__(parent, corner_radius=10, fg_color="#121212")
        self.parent = parent

        self.song_list = tk.Listbox(
            self,
            borderwidth=10,
            activestyle="none",
            width=34,
            height=16,
            relief="flat",
            bg="#141414",
            fg="#e0e0e0",
            selectbackground="#3aafa9",
            font=("roboto", 12),
            border=100,
            bd=10,
            highlightthickness=0,
        )
        self.song_list.grid(column=0, row=0, sticky="nesw")

        self.scrollbar = ctk.CTkScrollbar(self, command=self.song_list.yview)
        self.scrollbar.grid(column=0, row=0, sticky="nes")

        self.song_list.config(yscrollcommand=self.scrollbar.set)
        self.song_list.bind("<Double-1>", self.play)
        self.song_list.bind("<Return>", self.play)

    # SELECTION CALLBACK
    def play(self, event):
        try:
            index = event.widget.curselection()[0]
            self.parent.load_and_play_song(index)
        except IndexError:
            pass
