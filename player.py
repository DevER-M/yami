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
        self.play_icon = tk.PhotoImage(file="play_arrow.png").subsample(2, 2)
        self.pause_icon = tk.PhotoImage(file="pause.png").subsample(2, 2)
        self.playlist = []
        self.current_folder = ""
        self.playlist_index = 0
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        # setup
        self.is_playing = False
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.music

        self.open_folder = ttk.Button(
            self.root, command=self.choose_folder, text="Open", width=10
        )

        self.scrollbar = ttk.Scrollbar(self.root)

        self.song_list = tk.Listbox(
            self.root,
            borderwidth=5,
            yscrollcommand=self.scrollbar.set,
            activestyle="dotbox",
            width=30,
            listvariable=self.playlist,
        )

        self.play_button = ttk.Button(
            self.root,
            command=self.play_pause,
            text="play",
            width=10,
            image=self.pause_icon,
        )
        # widget placement
        self.play_button.grid(row=2, column=0, sticky="sw")
        self.open_folder.grid(row=0, column=0, sticky="nw")
        self.scrollbar.grid(row=0, column=2, sticky="nes", pady=30)
        self.song_list.grid(row=0, column=2, sticky="nes", pady=30, padx=15)
        # binding events
        self.song_list.bind("<<ListboxSelect>>", self.play)
        self.root.bind("<<NextSong>>", self.play_next_song)
        self.root.after(100, self.check_for_events)

    def play(self, event):
        self.music.stop()
        self.playlist_index = event.widget.curselection()[0]
        self.load_and_play_song(self.playlist_index)

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
        self.current_folder = filedialog.askdirectory(title="Select Music Folder")
        self.song_list.delete(0, tk.END)
        if self.current_folder:
            for file in filter(
                lambda x: (
                    x
                    if os.path.isfile(x)
                    and x.endswith((".mp3", ".ogg", ".wav", ".m4a", ".opus"))
                    else None
                ),
                os.listdir(self.current_folder),
            ):
                self.playlist.append(file)
                self.song_list.insert("end", file)

    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.root.event_generate("<<NextSong>>")
        self.root.after(100, self.check_for_events)

    def play_next_song(self, event=None):
        self.playlist_index = (self.playlist_index + 1) % len(self.playlist)
        self.load_and_play_song(self.playlist_index)

    def load_and_play_song(self, index):
        print(self.playlist)
        self.music.load(self.playlist[index])
        self.music.play()


root = ttk.Window(themename="darkly")
music_player = MusicPlayer(root)
root.mainloop()
