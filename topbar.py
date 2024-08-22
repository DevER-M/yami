import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import os
from pathlib import Path
from util import SUPPORTED_FORMATS


class TopBar(ctk.CTkFrame):
    def __init__(self, parent, folder_icon, music_icon):
        super().__init__(parent, fg_color="#121212")

        self.parent = parent

        # WIDGETS
        self.open_folder = ctk.CTkButton(
            self,
            command=self.choose_folder,
            text="Open",
            font=("roboto", 15),
            width=70,
            image=folder_icon,
        )
        self.ytdl_placeholder = ctk.CTkButton(
            self, text="Download", font=("roboto", 15), width=70, image=music_icon
        )

        # WIDGET PLACEMENT
        self.open_folder.grid(row=0, column=0, sticky="w", pady=5, padx=10)
        self.ytdl_placeholder.grid(row=0, column=1, sticky="w", pady=5, padx=10)

        # BINDINGS
        self.parent.bind("<Control-o>", self.choose_folder)

    # FOR ADDING SONGS TO PLAYLIST
    def choose_folder(self, _event=None):
        self.parent.current_folder = filedialog.askdirectory(
            title="Select Music Folder"
        )
        if not self.parent.current_folder:
            return

        # CLEAR PLAYLIST AND LISTBOX
        self.parent.playlist_frame.song_list.delete(0, tk.END)
        self.parent.playlist.clear()

        # FILTER MUSIC FILES
        for root, _, files in os.walk(self.parent.current_folder):
            music_files = [file for file in files if file.endswith(SUPPORTED_FORMATS)]

            for file in music_files:
                file_path = os.path.join(root, file)
                self.parent.playlist.append(file_path)
                self.parent.playlist_frame.song_list.insert(
                    "end", f"• {Path(file).stem}"
                )
