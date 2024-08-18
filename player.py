import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import os
import pygame
from enum import Enum
from mutagen import File
from PIL import Image


GEOMETRY = "800x500"
TITLE = "Music Player"
EVENT_INTERVAL = 100
SUPPORTED_FORMATS = (".mp3", ".ogg", ".wav", ".m4a", ".opus")
BUTTON_WIDTH = 10


class PlayerState(Enum):
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3


ctk.set_default_color_theme("theme.json")


class MusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()

        # CONFIG
        self.geometry(GEOMETRY)
        self.title(TITLE)

        # STATE
        self.playlist = []
        self.state = PlayerState.STOPPED
        self.current_folder = ""
        self.playlist_index = 0

        # SETUP PYGAME
        self.initialize_pygame()

        # ICONS
        self.play_icon = ctk.CTkImage(Image.open("play_arrow.png"))
        self.pause_icon = ctk.CTkImage(Image.open("pause.png"))
        self.prev_icon = ctk.CTkImage(Image.open("skip_prev.png"))
        self.next_icon = ctk.CTkImage(Image.open("skip_next.png"))

        # FRAMES
        self.control_bar = ControlBar(
            self, 
            self.pause_icon, 
            self.play_icon, 
            self.prev_icon,
            self.next_icon,
            self.play_next_song
        )
        self.playlist_frame = PlaylistFrame(self)
        self.topbar = TopBar(self)
        self.bottom_frame = BottomFrame(self)

        # BINDINGS AND EVENTS
        self.bind("<F10>", self.play_next_song)
        self.bind("<F8>",self.control_bar.play_previous)
        self.bind("<F9>",self.control_bar.play_pause)
        self.bind("<space>",self.control_bar.play_pause)
        self.after(100, self.check_for_events)

        # WIDGET PLACEMENT
        self.topbar.pack(side=tk.TOP, fill=tk.X)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.control_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.playlist_frame.pack(side=tk.RIGHT)

    def play_next_song(self,event=None):
        if not self.playlist:
            return

        # PLAY FROM BEGINING
        elif self.playlist_index >= len(self.playlist) - 1:
            self.playlist_index = 0
        else:
            self.playlist_index += 1
        self.load_and_play_song(self.playlist_index)

        # UPDATE SELECTION
        self.playlist_frame.song_list.selection_clear(0, tk.END)
        self.playlist_frame.song_list.select_set(self.playlist_index)

    def load_and_play_song(self, index):
        self.music.unload()
        self.music.stop()
        self.music.load(self.playlist[index])
        self.music.play()
        self.state = PlayerState.PLAYING
        self.control_bar.update_play_button(self.state)
        self.bottom_frame.start_progress_bar(self.get_song_length(self.playlist[index]))

    def get_song_length(self, file_path):
        audio = File(file_path)
        if audio is not None and audio.info is not None:
            return audio.info.length
        else:
            return 0

    def get_song_position(self):
        return pygame.mixer.music.get_pos() / 1000

    def initialize_pygame(self):
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.music

        #CREATE USEREVENT WHEN MUSIC ENDS
        pygame.mixer.music.set_endevent(pygame.USEREVENT) 

    # AUTOPLAY NEXT SONG AFTER SONG ENDS
    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.play_next_song()
        self.after(EVENT_INTERVAL, self.check_for_events)


class ControlBar(ctk.CTkFrame):
    def __init__(
            self, 
            parent: MusicPlayer, 
            pause_icon, 
            play_icon, 
            prev_icon,
            next_icon,
            play_next_command
            ):
        super().__init__(parent,corner_radius=10,fg_color="#141414")

        # SETUP
        self.music_player = parent
        self.pause_icon = pause_icon
        self.play_icon = play_icon
        self.play_next_command = play_next_command

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
            image=next_icon
        )
        self.prev_button = ctk.CTkButton(
            self,
            text="",
            width=BUTTON_WIDTH,
            corner_radius=10,
            command=self.play_previous,
            image=prev_icon
        )

        # PLACEMENT
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=0)  
        self.grid_columnconfigure(2, weight=0)  
        self.grid_columnconfigure(3, weight=0)  
        self.grid_columnconfigure(4, weight=1)  

        # PLACEMENT
        self.prev_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)
        self.play_button.grid(row=0, column=2, sticky="nsew", padx=5, pady=10)
        self.next_button.grid(row=0, column=3, sticky="nsew", padx=5, pady=10)

    def play_pause(self,event=None):
        if self.music_player.state == PlayerState.PLAYING:
            self.music_player.music.pause()
            self.music_player.state = PlayerState.PAUSED
        else:
            self.music_player.music.unpause()
            self.music_player.state = PlayerState.PLAYING
        self.update_play_button(self.music_player.state)

    def update_play_button(self, state):
        if state == PlayerState.PLAYING:
            self.play_button.configure(image=self.pause_icon)
        else:
            self.play_button.configure(image=self.play_icon)
            

    def play_previous(self,event=None):
        if not self.music_player.playlist:
            return

        # PLAY FROM END
        elif self.music_player.playlist_index == 0:
            self.music_player.playlist_index = len(self.music_player.playlist) - 1
        #PLAY PREVIOUS
        else:
            self.music_player.playlist_index -= 1
        self.music_player.load_and_play_song(self.music_player.playlist_index)

        # UPDATE SELECTION
        self.music_player.playlist_frame.song_list.selection_clear(0, tk.END)
        self.music_player.playlist_frame.song_list.select_set(
            self.music_player.playlist_index
        )


class BottomFrame(ctk.CTkFrame):
    def __init__(self, parent: MusicPlayer):
        super().__init__(parent)
        
        #SETUP
        self.music_player = parent
        
        self.progress_bar = ctk.CTkProgressBar(self,progress_color="#1f0469")
        self.progress_bar.pack(fill="x", expand=True)
        self.progress_bar.set(0)
        
        self.pack(fill="x")#IMP

    def start_progress_bar(self, song_length):
        self.progress_bar.set(0)
        self.song_length = song_length
        self.update_progress_bar()
    
    #PARTIALY WORKING
    def update_progress_bar(self):
        if self.music_player.state == PlayerState.PLAYING:
            song_position = self.music_player.get_song_position()
            progress = song_position / self.song_length
            self.progress_bar.set(progress)
            if song_position < self.song_length:
                self.after(EVENT_INTERVAL, self.update_progress_bar)
        elif self.music_player.state == PlayerState.PAUSED:
            # Keep updating the progress bar even in the paused state
            self.after(EVENT_INTERVAL, self.update_progress_bar)
        else:
            # Stop updating the progress bar when the song is stopped
            self.progress_bar.set(0)


class PlaylistFrame(ctk.CTkFrame):
    def __init__(self, parent: MusicPlayer):
        super().__init__(parent,corner_radius=10,fg_color="#141414")
        self.parent = parent

        self.song_list = tk.Listbox(
            self, 
            borderwidth=5, 
            activestyle="dotbox", 
            width=30, 
            height=15,
            relief="flat",
            bd=10,
            bg="#141414",
            fg="#FFFFFF",
            selectbackground="#1f0469",
            font=("roboto",12)
        )
        self.song_list.grid(column=0, row=0, sticky="nesw")

        self.scrollbar = ctk.CTkScrollbar(self, command=self.song_list.yview)
        self.scrollbar.grid(column=0, row=0, sticky="nes")

        self.song_list.config(yscrollcommand=self.scrollbar.set)
        self.song_list.bind("<Double-1>", self.play)
        self.song_list.bind("<Return>",self.play)

    def play(self, event):
        try:
            index = event.widget.curselection()[0]
            self.parent.load_and_play_song(index)
        except IndexError:
            pass


class TopBar(ctk.CTkFrame):
    def __init__(self, parent: MusicPlayer):
        super().__init__(parent, fg_color="#141414")
        
        self.parent = parent
        
        # WIDGETS
        self.open_folder = ctk.CTkButton(
            self,
            command=self.choose_folder,
            text="Open",
            font=("roboto", 15),
            width=70,
        )
        self.ytdl_placeholder = ctk.CTkButton(
            self, 
            text="Download", 
            font=("roboto", 15), 
            width=70
        )

        # WIDGET PLACEMENT
        self.open_folder.grid(row=0, column=0, sticky="w", pady=5, padx=10)
        self.ytdl_placeholder.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        
        # BINDINGS
        self.parent.bind("<Control-o>", self.choose_folder)

    # FOR ADDING SONGS TO PLAYLIST
    def choose_folder(self, _event=None):
        self.current_folder = filedialog.askdirectory(title="Select Music Folder")

        # CLEAR PLAYLIST AND LISTBOX
        self.parent.playlist_frame.song_list.delete(0, tk.END)
        self.parent.playlist.clear()

        # FILTER MUSIC FILES
        if self.current_folder:
            for file in filter(
                lambda x: (
                    x if os.path.isfile(x) and x.endswith(SUPPORTED_FORMATS) else None
                ),
                os.listdir(self.current_folder),
            ):
                self.parent.playlist.append(file)
                self.parent.playlist_frame.song_list.insert("end", f"• {file}")


if __name__ == "__main__":
    music_player = MusicPlayer()
    music_player.mainloop()
    
