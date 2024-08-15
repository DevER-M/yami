import ttkbootstrap as ttk
from tkinter import filedialog
import tkinter as tk
import os
import pygame


class MusicPlayer:
    def __init__(self,root:ttk.Window):
        # basic config
        self.root = root
        self.root.geometry("800x500")
        self.root.columnconfigure(0,weight=2)
        self.root.columnconfigure(1,weight=1)
        self.root.columnconfigure(2,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        self.root.rowconfigure(2,weight=1)
        self.root.title = "Music Player"
        self.current_song_index = 0
        self.playlist = []
        self.is_playing = False
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.music


        open_folder = ttk.Button(self.root,command=self.choose_folder,text="Open",width=10)
        open_folder.grid(row=0,column=0,sticky="nw")

        scrollbar = ttk.Scrollbar(self.root)
        scrollbar.grid(row=0,column=2,sticky="nes",pady=30)
             
        self.song_list = tk.Listbox(self.root,borderwidth=50,yscrollcommand=scrollbar.set)
        self.song_list.grid(row=0, column=2,sticky="nes",pady=30,padx=15)

        play_button = ttk.Button(self.root,command=self.play_pause,text="play",width=10)
        play_button.grid(row=2,column=0)

        
    def play_pause(self):
        print(self.song_list.get(self.song_list.curselection()[0]))
        self.music.load(open(self.song_list.get(self.song_list.curselection()[0]),"rb"))
        self.music.play()


    def choose_folder(self):
        folder = filedialog.askdirectory(title="Select Music Folder")
        for file in filter(lambda x:x if os.path.isfile(x) else None,os.listdir(folder)):
            self.song_list.insert("end",file)

        
root=ttk.Window(themename="darkly")
music_player = MusicPlayer(root)
root.mainloop()
        