import ttkbootstrap as ttk
from tkinter import filedialog
import tkinter as tk
import os
import pygame


class MusicPlayer(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.geometry("800x500")
        self.title("Music Player")
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.play_icon = ttk.PhotoImage(file="play_arrow.png").subsample(2, 2)
        self.pause_icon = ttk.PhotoImage(file="pause.png").subsample(2, 2)
        self.playlist = []
        self.current_folder = ""
        self.playlist_index = 0

        # setup
        self.is_playing = False
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.music
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.bottom_bar = BottomBar(self, self.pause_icon, self.play_pause)

        self.open_folder = ttk.Button(
            self, command=self.choose_folder, text="Open", width=10
        )

        self.scrollbar = ttk.Scrollbar(self)

        self.song_list = tk.Listbox(
            self,
            borderwidth=5,
            yscrollcommand=self.scrollbar.set,
            activestyle="dotbox",
            width=30,
        )

        # widget placement
        self.open_folder.grid(row=0, column=0, sticky="nw")
        self.scrollbar.grid(row=0, column=2, sticky="nes", pady=30)
        self.song_list.grid(row=0, column=2, sticky="nes", pady=30, padx=15)
        self.bottom_bar.grid(row=3,column=0,sticky="nsew")
        # binding events
        self.song_list.bind("<<ListboxSelect>>", self.play)
        self.bind("<<NextSong>>", self.play_next_song)
        self.after(100, self.check_for_events)

    def play(self, event):
        self.music.stop()
        print(event.widget.curselection()[0])
        self.playlist_index = event.widget.curselection()[0]
        self.load_and_play_song(self.playlist_index)

    def choose_folder(self):
        self.current_folder = filedialog.askdirectory(title="Select Music Folder")
        self.song_list.delete(0, tk.END)
        self.playlist.clear()
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
                self.event_generate("<<NextSong>>")
        self.after(100, self.check_for_events)

    def play_next_song(self, event=None):
        if self.playlist_index == len(self.playlist):
            pass
        if self.playlist_index >= len(self.playlist):
            self.playlist_index = 0
        else:
            self.playlist_index = self.playlist_index + 1
            self.load_and_play_song(self.playlist_index)
            self.song_list.activate(self.playlist_index)

    def load_and_play_song(self, index):
        if index == 0:
            self.music.load(self.playlist[index])
        else:
            self.music.load(self.playlist[index - 1])
        self.music.play()

    def play_pause(self):
        if not self.is_playing:
            self.bottom_bar.play_button.config(image=self.pause_icon)
            self.music.unpause()
            self.is_playing = True
        else:
            self.music.pause()
            self.bottom_bar.play_button.config(image=self.play_icon)
            self.is_playing = False


class BottomBar(ttk.Frame):
    def __init__(self, parent, pause_icon, play_command):
        super().__init__(parent)

        self.play_button = ttk.Button(
            self,
            command=play_command,
            width=10,
            image=pause_icon,
        )

        self.play_button.grid(row=0, column=0, sticky="sw")


music_player = MusicPlayer()
music_player.mainloop()
