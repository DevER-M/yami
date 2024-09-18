import customtkinter as ctk
import tkinter as tk


class PlaylistFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10, fg_color="#121212")
        self.parent = parent

        self.song_list = tk.Listbox(
            self,
            borderwidth=5,
            activestyle="dotbox",
            width=32,
            height=18,
            relief="flat",
            bd=10,
            bg="#121212",
            fg="#FFFFFF",
            selectbackground="#1f0469",
            font=("roboto", 12),
        )
        self.song_list.grid(column=0, row=0, sticky="nesw")

        self.scrollbar = ctk.CTkScrollbar(self, command=self.song_list.yview)
        self.scrollbar.grid(column=0, row=0, sticky="nes")

        self.song_list.config(yscrollcommand=self.scrollbar.set)
        self.song_list.bind("<Double-1>", self.play)
        self.song_list.bind("<Return>", self.play)

    #SELECTION CALLBACK
    def play(self, event):
        try:
            index = event.widget.curselection()[0]
            self.parent.load_and_play_song(index)
        except IndexError:
            pass
