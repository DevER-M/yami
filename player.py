import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import os
import pygame
from enum import Enum
from mutagen import File
from PIL import Image


GEOMETRY          = "800x500"
TITLE             = "Music Player"
EVENT_INTERVAL    = 100
SUPPORTED_FORMATS = (".mp3", ".ogg", ".wav", ".m4a", ".opus")
BUTTON_WIDTH      = 10
THEME             = "darkly"


class PlayerState(Enum):
    PLAYING = 1
    PAUSED  = 2
    STOPPED = 3

ctk.set_default_color_theme("theme.json")
class MusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()

        #CONFIG
        self.geometry(GEOMETRY)
        self.title(TITLE)
        

        # STATE
        self.playlist       = []
        self.state          = PlayerState.STOPPED
        self.current_folder = ""
        self.playlist_index = 0

        #SETUP PYGAME
        self.initialize_pygame()

        #ICONS
        self.play_icon = ctk.CTkImage(Image.open("play_arrow.png"))
        self.pause_icon = ctk.CTkImage(Image.open("pause.png"))

        #FRAMES
        self.bottom_bar = BottomBar(
            self, 
            self.pause_icon, 
            self.play_icon, 
            self.play_next_song
        )
        self.playlist_frame = PlaylistFrame(self)
        self.topbar = TopBar(self)
        
        #BINDINGS AND EVENTS
        self.bind("<F10>", self.play_next_song)
        self.after(100, self.check_for_events)
        
        #WIDGET PLACEMENT
        self.topbar.pack(side=tk.TOP,fill=tk.X)
        self.bottom_bar.pack(side=tk.BOTTOM,fill=tk.X)
        self.playlist_frame.pack(side=tk.RIGHT)
        

    
    

    def play_next_song(self, event=None):
        if not self.playlist:
            return
        
        #PLAY FROM BEGINING
        elif self.playlist_index >= len(self.playlist) -1:
            self.playlist_index = 0
        else:
            self.playlist_index += 1  
        self.load_and_play_song(self.playlist_index)

        #UPDATE SELECTION
        self.playlist_frame.song_list.selection_clear(0, tk.END)
        self.playlist_frame.song_list.select_set(self.playlist_index)         

    def load_and_play_song(self, index):
        self.music.unload()
        self.music.stop()
        self.music.load(self.playlist[index])
        self.music.play()
        self.state = PlayerState.PLAYING
        self.bottom_bar.update_play_button(self.state)
        self.bottom_bar.start_progress_bar(self.get_song_length(self.playlist[index]))
    
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
        pygame.mixer.music.set_endevent(pygame.USEREVENT)                     #CREATE USEREVENT WHEN MUSIC ENDS

    #AUTOPLAY NEXT SONG AFTER SONG ENDS
    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.play_next_song()
        self.after(EVENT_INTERVAL, self.check_for_events)


class BottomBar(ctk.CTkFrame):
    def __init__(self, parent: MusicPlayer, pause_icon, play_icon, play_next_command):
        super().__init__(parent)
        
        #SETUP
        self.music_player      = parent
        self.pause_icon        = pause_icon
        self.play_icon         = play_icon
        self.play_next_command = play_next_command

        #WIDGETS
        self.play_button = ctk.CTkButton(
            self,
            command = self.play_pause,
            width   = BUTTON_WIDTH,
            height  = 10,
            text    = "",
            image   = pause_icon,
            corner_radius=10
        )
        self.next_button = ctk.CTkButton(
            self, 
            command = play_next_command, 
            width   = BUTTON_WIDTH, 
            text    = "next",
            corner_radius=10
        )
        """self.progress_bar = ctk.CTkProgressBar(
            self, 
            mode="determinate", 
            width=600
            )"""
        self.prev_button = ctk.CTkButton(
            self,
            text="prev",
            width=BUTTON_WIDTH,
            corner_radius=10
        )

        self.bottom_frame = BottomFrame(self)
        
        
        #PLACEMENT
        #self.prev_button.grid(row=1,column=0,sticky="nsew")
        #self.play_button.grid(row=1, column=1, sticky="nsew")
        #self.next_button.grid(row=1, column=2, sticky="nsew",)
        #self.progress_bar.grid(row=3,column=4, sticky="senw")
        self.bottom_frame.pack(side="bottom")


    def play_pause(self):
        if self.music_player.state == PlayerState.PLAYING:
            self.music_player.music.pause()
            self.music_player.state = PlayerState.PAUSED
        else:
            self.music_player.music.unpause()
            self.music_player.state = PlayerState.PLAYING
        self.update_play_button(self.music_player.state)

    def update_play_button(self, state):
        if state == PlayerState.PLAYING:
            self.play_button.config(image=self.pause_icon)
        else:
            self.play_button.config(image=self.play_icon)

    def start_progress_bar(self, song_length):
        self.progress_bar["maximum"] = song_length
        self.update_progress_bar()

    def update_progress_bar(self):
        if self.music_player.state == PlayerState.PLAYING:
            song_position = self.music_player.get_song_position()
            self.progress_bar["value"] = song_position
            if song_position < self.progress_bar["maximum"]:
                self.after(EVENT_INTERVAL, self.update_progress_bar)

class BottomFrame(ctk.CTkFrame):
    def __init__(self,parent:BottomBar):
        super().__init__(parent)
        self.parent = parent
        

        self.progress_bar = ctk.CTkProgressBar(self, progress_color="green")
        self.progress_bar.pack(fill="x",expand=True)
        self.pack(fill="x")


class PlaylistFrame(ctk.CTkFrame):
    def __init__(self, parent: MusicPlayer):
        super().__init__(parent)
        self.parent = parent

        self.song_list = tk.Listbox(
            self, 
            borderwidth=5, 
            activestyle="dotbox", 
            width=30, 
            height=15, 
            border=10
        )
        self.song_list.grid(column=0, row=0, sticky="nesw")

        self.scrollbar = ctk.CTkScrollbar(self, command=self.song_list.yview)
        self.scrollbar.grid(column=0, row=0, sticky="nes")

        self.song_list.config(yscrollcommand=self.scrollbar.set)
        self.song_list.bind("<<ListboxSelect>>", self.play)

    def play(self, event):
        index = event.widget.curselection()[0]
        self.parent.load_and_play_song(index)



class TopBar(ctk.CTkFrame):
    def __init__(self,parent:MusicPlayer):
        super().__init__(parent,fg_color="#141414")
        self.parent = parent
        #WIDGETS
        self.open_folder = ctk.CTkButton(
            self, 
            command=self.choose_folder, 
            text="Open",
            font=("roboto",15),
            width=70,
            
        )
        self.ytdl_placeholder = ctk.CTkButton(
            self,
            text="Download",
            font=("roboto",15),
            width=70
        )

        #WIDGET PLACEMENT
        self.open_folder.grid(row=0,column=0,sticky="w",pady=5,padx=10)
        self.ytdl_placeholder.grid(row=0,column=1,sticky="w",pady=5,padx=10)
        #BINDINGS
        self.bind("<Control-o>", self.choose_folder)
    
    #FOR ADDING SONGS TO PLAYLIST
    def choose_folder(self, _event=None):
        self.current_folder = filedialog.askdirectory(title="Select Music Folder")
        
        #CLEAR PLAYLIST AND LISTBOX
        self.parent.playlist_frame.song_list.delete(0, tk.END)
        self.playlist.clear()
        
        #FILTER MUSIC FILES
        if self.current_folder:
            for file in filter(
                lambda x: (
                    x if os.path.isfile(x) and x.endswith(SUPPORTED_FORMATS) else None
                ),
                os.listdir(self.current_folder),
            ):
                self.playlist.append(file)
                self.playlist_frame.song_list.insert("end", file)


if __name__ == "__main__":
    music_player = MusicPlayer()
    music_player.mainloop()
