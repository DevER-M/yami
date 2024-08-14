from ttkbootstrap import ttk
from tkinter import Tk,filedialog
import tkinter as tk



class MusicPlayer:
    def __init__(self,root:Tk):
        self.root = root
        self.root.geometry("800x500")
        self.root.configure(background="black")
        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(1,weight=1)
        self.root.columnconfigure(2,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)

        self.root.title = "Music Player"
        self.current_song_index = 0
        self.playlist = []
        self.is_playing = False

        open_folder = ttk.Button(self.root,command=filedialog.askdirectory,text="Open")

        open_folder.grid(row=0,column=0)
        
        scrollbar = ttk.Scrollbar(self.root)
        self.song_list = tk.Listbox(self.root, bg="white", fg="black", selectbackground="yellow", selectforeground="gray", yscrollcommand=scrollbar.set)
        self.song_list.grid(row=0, column=8, columnspan=3, padx=10, pady=10)
        
        scrollbar.grid(row=0,column=5,)

root=Tk()
music_player = MusicPlayer(root)
root.mainloop()
        