import ttkbootstrap as ttk
from tkinter import filedialog
import tkinter as tk
import os
import pygame


class MusicPlayer:
    def __init__(self, root: ttk.Window):
        # basic config
        self.root = root
        self.root.geometry("800x500")
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.title = "Music Player"
        self.is_playing = False
        self.play_icon = tk.PhotoImage(file="play_arrow.png").subsample(2, 2)
        self.pause_icon = tk.PhotoImage(file="pause.png").subsample(2, 2)
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.music

        self.open_folder = ttk.Button(
            self.root, command=self.choose_folder, text="Open", width=10
        )
        self.open_folder.grid(row=0, column=0, sticky="nw")

        self.scrollbar = ttk.Scrollbar(self.root)
        self.scrollbar.grid(row=0, column=2, sticky="nes", pady=30)

        self.song_list = tk.Listbox(
            self.root, borderwidth=50, yscrollcommand=self.scrollbar.set
        )
        self.song_list.bind("<<ListboxSelect>>", self.play)
        self.song_list.grid(row=0, column=2, sticky="nes", pady=30, padx=15)

        self.play_button = ttk.Button(
            self.root,
            command=self.play_pause,
            text="play",
            width=10,
            image=self.pause_icon,
        )
        self.play_button.grid(row=2, column=0, sticky="sw")

    def play(self, event):
        for e in event.widget.curselection():
            self.music.load(open(self.song_list.get(e), "rb"))
        self.music.play()

    def play_pause(self):
        if not self.is_playing:
            self.play_button.config(image=self.pause_icon)
            self.music.unpause()
            self.is_playing = True
        else:
            self.music.pause()
            self.play_button.config(image=self.play_icon)
            self.is_playing = False

    def choose_folder(self):
        folder = filedialog.askdirectory(title="Select Music Folder")
        self.song_list.delete(0, tk.END)
        if folder:
            for file in filter(
                lambda x: (
                    x
                    if os.path.isfile(x)
                    and x.endswith((".mp3", ".ogg", ".wav", ".m4a", ".opus"))
                    else None
                ),
                os.listdir(folder),
            ):
                self.song_list.insert("end", file)


root = ttk.Window(themename="darkly")
music_player = MusicPlayer(root)
root.mainloop()
