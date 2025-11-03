"""Root Widget"""

from pathlib import Path
import tkinter as tk
import tempfile
import asyncio
import logging


from mutagen import File, id3
import customtkinter as ctk
from PIL import Image, ImageDraw
import spotdl
import vlc


from .topbar import TopBar
from .playlist import PlaylistFrame
from .control import ControlBar
from .cover_art import CoverArtFrame
from .progress import BottomFrame
from .util import GEOMETRY, TITLE, PlayerState, EVENT_INTERVAL, make_time_string


ctk.set_default_color_theme("yami/data/theme.json")
ctk.set_appearance_mode("dark")


class MusicPlayer(ctk.CTk):
    """ROOT"""

    def __init__(self: ctk.CTk, loop=None):
        """ROOT INIT"""
        super().__init__()

        # CONFIG
        self.geometry(GEOMETRY)
        self.title(TITLE)

        # STATE
        self.playlist = []
        self.current_folder = ""

        self.loop = loop if loop is not None else asyncio.new_event_loop()
        self.downloader = spotdl.Downloader(spotdl.DownloaderOptions(threads=2))
        spotdl.SpotifyClient.init(
            "5f573c9620494bae87890c0f08a60293",
            "212476d9b0f3472eaa762d90b19b0ba8",
        )

        self.initialize_vlc()

        # TKINTER SETUP
        self.setup_icons()
        self.setup_frames()
        self.setup_widget_packing()

        self.setup_keybindings()

        self.event_manager = self.music_list_player.event_manager()
        self.event_manager.event_attach(
            vlc.EventType.MediaListPlayerNextItemSet, self.change_info
        )
        self.update_loop()
        self.after(EVENT_INTERVAL, self.update)

    def update(self, event=None):
        if self.music_list_player.get_state() == vlc.State.Playing:

            song_position = self.music.get_position()
            self.bottom_frame.progress_bar.set(song_position)

            self.control_bar.playback_label.configure(
                text=make_time_string(song_position, self.music.get_length() // 1000)
            )
        self.after(EVENT_INTERVAL, self.update)

    def load_and_play_song(self, index):

        self.music_list_player.pause()
        self.music_list_player.play_item_at_index(index)
        self.playlist_index = index

        # CHANGE INFO
        self.change_info()

        logging.debug("playing %s", self.get_song_title())

    def change_info(self, event=None):
        logging.debug("changing art,name of this song")

        self.cover_art_frame.cover_art_label.configure(
            require_redraw=True, image=self.get_album_cover(), fg_color="#121212"
        )
        self.control_bar.set_music_title(  # truncates longer titles
            self.get_song_title(),
            self.get_song_artist(),
        )
        self.control_bar.update_play_button()

    def play_next_song(self, _event=None):
        logging.debug("playing next song due to button press / keybind")
        self.music_list_player.next()
        self.change_info()
        # UPDATE SELECTION
        self.playlist_frame.song_list.selection_clear(0, tk.END)
        self.playlist_index+=1
        self.playlist_frame.song_list.select_set(self.playlist_index)

    def play_previous(self, event=None):
        logging.debug("playing previous song due to button press / keybind")
        self.music_list_player.previous()
        self.change_info()
        # UPDATE SELECTION
        self.playlist_frame.song_list.selection_clear(0, tk.END)
        self.playlist_index-=1
        self.playlist_frame.song_list.select_set(self.playlist_index)

    def get_song_length(self) -> int:
        logging.debug("got song length")
        return self.music.get_length()

    def get_song_title(self) -> str:
        media = self.music_list_player.get_media_player().get_media()
        logging.debug("got song title")
        try:
            if media.is_parsed():
                return media.get_meta(0)
            else:
                media.parse()
                return media.get_meta(0)
        except Exception as e:
            logging.exception(e)
            return ""

    def get_album_cover(self) -> ctk.CTkImage | None:
        try:
            media = self.music_list_player.get_media_player().get_media()
            media.parse()
            logging.debug("got album cover")
            return ctk.CTkImage(
                self.round_corners(
                    Image.open(
                        Path.from_uri(media.get_meta(15))
                    ),  # gives the direct uri to cover jpg
                    20,
                ),
                size=(250, 250),
            )
        except Exception as e:
            logging.exception(e)
            return
        return

    def get_song_artist(self) -> str:
        media = self.music_list_player.get_media_player().get_media()
        logging.debug("got song artist")
        try:
            if media.is_parsed():
                return media.get_meta(1)
            else:
                media.parse()
                return media.get_meta(1)
        except Exception as e:
            logging.exception(e)
            return ""

    def get_song_position(self) -> float:
        return self.music.get_position()

    def round_corners(self, image, radius) -> Image.Image:
        """Rounds Album Cover"""
        rounded_mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(rounded_mask)
        draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)

        rounded_image = Image.new("RGBA", image.size)
        rounded_image.paste(image, (0, 0), mask=rounded_mask)
        logging.debug("rounded album cover")

        return rounded_image

    def initialize_vlc(self):
        """initializes and creates
        :param `self.music_list_player`: vlc.MediaListPlayer
        :param `self.music`:             vlc.MediaPlayer
        :param `self.vlc_instance`:      vlc.Instance
        :returns: some vlc attributes
        """
        self.music_list_player: vlc.MediaListPlayer = vlc.MediaListPlayer()
        self.music: vlc.MediaPlayer = self.music_list_player.get_media_player()
        self.vlc_instance: vlc.Instance = self.music_list_player.get_instance()
        logging.debug("initialized vlc")

    def setup_icons(self):
        self.play_icon = ctk.CTkImage(Image.open("yami/data/play_arrow.png"))
        self.pause_icon = ctk.CTkImage(Image.open("yami/data/pause.png"))
        self.prev_icon = ctk.CTkImage(Image.open("yami/data/skip_prev.png"))
        self.next_icon = ctk.CTkImage(Image.open("yami/data/skip_next.png"))
        self.folder_icon = ctk.CTkImage(Image.open("yami/data/folder.png"))
        self.music_icon = ctk.CTkImage(Image.open("yami/data/music.png"))
        logging.debug("icons setup")

    def setup_frames(self):
        self.topbar = TopBar(self)
        self.control_bar = ControlBar(self)
        self.playlist_frame = PlaylistFrame(self)
        self.bottom_frame = BottomFrame(self)
        self.cover_art_frame = CoverArtFrame(self)

    def setup_keybindings(self):
        """
        :param `<F9>`: play next
        :param `<F8>`: play previous
        :param `<Space>`:  play or pause
        """

        self.bind("<F10>", self.play_next_song)
        self.bind("<F8>", self.play_previous)
        self.bind("<F9>", self.control_bar.play_pause)
        self.bind("<space>", self.control_bar.play_pause)
        self.bind("<Control-o>", self.topbar.choose_folder)
        logging.debug("setup keybinds")

    def setup_widget_packing(self):
        self.topbar.pack(side=tk.TOP, fill=tk.X)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.control_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.playlist_frame.pack(side=tk.RIGHT)
        self.cover_art_frame.pack(side=tk.LEFT, padx=10)
        logging.debug("widgets packed")

    def update_loop(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        self.after(1000, self.update_loop)


if __name__ == "__main__":
    music_player = MusicPlayer()
    music_player.mainloop()
