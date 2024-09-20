import customtkinter as ctk
from tkinter import filedialog, simpledialog
import tkinter as tk
import os
from pathlib import Path
import spotdl.utils
import spotdl.utils.formatter
import spotdl.utils.search
from mus.util import SUPPORTED_FORMATS
import spotdl
import asyncio
import logging
from mus.game import BeatsGame
import multiprocessing

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
        self.music_downloader = ctk.CTkButton(
            self,
            text="Download",
            font=("roboto", 15),
            width=70,
            image=music_icon,
            command=self.prompt_download,
        )

        self.yami = ctk.CTkButton(
            self,
            text="Yami",
            font=("roboto", 15),
            width=70,
            image=music_icon,
            command=multiprocessing.Process(target=BeatsGame,daemon=False).start
        )

        # WIDGET PLACEMENT
        self.open_folder.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        self.music_downloader.grid(
            row=0, column=2, sticky="w", pady=5, padx=10
        )
        self.yami.grid(row=0, column=3, sticky="w", pady=5, padx=10)

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
            music_files = [
                file for file in files if file.endswith(SUPPORTED_FORMATS)
            ]

            for file in music_files:
                file_path = os.path.join(root, file)
                self.parent.playlist.append(file_path)
                self.parent.playlist_frame.song_list.insert(
                    "end", f"• {Path(file).stem}"
                )

    def prompt_download(self):
        if not self.parent.current_folder:
            self.choose_folder()
        song_url = simpledialog.askstring(
            "Download Music", "Enter the name of the song:"
        )
        if song_url:
            self.music_downloader.configure(state="disabled")
            self.parent.loop.create_task(self.download_song(song_url))

    async def download_song(self, song_url):
        try:
            logging.info(f"searching {song_url}")

            # ASYNC UNTIL DOWNLOAD GETS OVER
            song, path = await asyncio.ensure_future(
                asyncio.to_thread(
                    self.parent.downloader.search_and_download,
                    spotdl.utils.search.get_simple_songs([song_url])[0],
                )
            )
            await asyncio.sleep(0)  # STOP FROM FREEZING
            logging.info("saving file")
            downloaded_song_path = os.path.join(
                self.parent.current_folder,
                spotdl.utils.formatter.create_file_name(
                    song=song,
                    template=self.parent.downloader.settings["output"],
                    file_extension=self.parent.downloader.settings["format"],
                    restrict=self.parent.downloader.settings["restrict"],
                    file_name_length=self.parent.downloader.settings[
                        "max_filename_length"
                    ],
                ),
            )
            logging.info(f"saved at {downloaded_song_path}")
        except Exception as e:
            logging.error(e)
        finally:
            self.music_downloader.configure(state="normal")

        self.parent.playlist.append(downloaded_song_path)
        self.parent.playlist_frame.song_list.insert(
            "end", f"• {Path(downloaded_song_path).stem}"
        )
