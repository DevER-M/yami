import customtkinter as ctk
from tkinter import filedialog, simpledialog
import tkinter as tk
import os
from pathlib import Path
from mus.util import SUPPORTED_FORMATS
from spotdl import Spotdl
import asyncio
from async_tkinter_loop import async_handler


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
            self,
            text="Download",
            font=("roboto", 15),
            width=70,
            image=music_icon,
            command=self.prompt_download,
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

    def prompt_download(self):
        song_url = simpledialog.askstring(
            "Download Music", "Enter the URL of the song:"
        )
        if song_url:
            print("e")
            self.download_song(song_url)
    @async_handler
    async def download_song(self, song_url):
        # Create a Spotdl object
        print("eh")
        spotdl = Spotdl(
            "5f573c9620494bae87890c0f08a60293", "212476d9b0f3472eaa762d90b19b0ba8"
        )

        # Run the download process asynchronously
        song, path = spotdl.download(spotdl.search([song_url])[0])
        print(song)
        # Optional: Add the downloaded song to the playlist
        downloaded_song_path = os.path.join(self.current_folder, f"{song.name}.mp3")
        if os.path.exists(downloaded_song_path):
            self.parent.playlist.append(downloaded_song_path)
            self.parent.playlist_frame.song_list.insert(
                "end", f"• {Path(downloaded_song_path).stem}"
            )
