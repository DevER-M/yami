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
from .util import GEOMETRY, TITLE, PlayerState, EVENT_INTERVAL


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
        self.STATE = PlayerState.STOPPED
        self.current_folder = ""
        self.playlist_index = 0
        self.loop = loop if loop is not None else asyncio.new_event_loop()
        self.downloader = spotdl.Downloader(
            spotdl.DownloaderOptions(threads=4)
        )
        spotdl.SpotifyClient.init(
            "5f573c9620494bae87890c0f08a60293",
            "212476d9b0f3472eaa762d90b19b0ba8",
        )

        # SETUP PYGAME
        self.initialize_vlc()

        # ICONS
        self.setup_icons()

        # FRAMES
        self.topbar = TopBar(self)
        self.control_bar = ControlBar(self)
        self.playlist_frame = PlaylistFrame(self)
        self.bottom_frame = BottomFrame(self)
        self.cover_art_frame = CoverArtFrame(self)

        # BINDINGS AND EVENTS
        self.setup_bindings()

        # WIDGET PLACEMENT
        self.topbar.pack(side=tk.TOP, fill=tk.X)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.control_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.playlist_frame.pack(side=tk.RIGHT)
        self.cover_art_frame.pack(side=tk.LEFT, padx=10)

        # UPDATE LOOP
        self.after(EVENT_INTERVAL, self.update)
        self.update_loop()

    def update(self):
        if self.music.get_state()== vlc.State.Opening:
            self.after(EVENT_INTERVAL, self.update)

        
        if self.music.get_state() == vlc.State.Playing:
            song_position = self.get_song_position()
            self.song_length=self.music.get_length()//1000
            
            curtime=song_position*self.music.get_length()//1000
            #print(curtime,song_position,self.music.get_length())

            # GETS RATIO OF PROGRESS
            #progress = song_position / self.song_length
            self.bottom_frame.progress_bar.set(song_position)

            minutes = int(curtime // 60)  # logic wrong 
            seconds = int(curtime % 60)

            song_min = int(self.song_length // 60)
            song_sec = int(self.song_length % 60)

            time_string = (
                f"{minutes:02d}:{seconds:02d} / {song_min:02d}:{song_sec:02d}"
            )
            self.control_bar.playback_label.configure(text=time_string)

            #if self.music.get_state()==vlc.State.Ended: # check is still song is not over or not song position less than song length means not yet reached end
             #   print("hi")
            self.after(EVENT_INTERVAL, self.update)
        elif self.music.get_state()==vlc.State.Ended:
            self.play_next_song()

        elif self.music.get_state() == vlc.State.Paused:
            self.after(EVENT_INTERVAL, self.update)
        else:
            self.bottom_frame.progress_bar.set(0)

    def load_and_play_song(self, index):
        try:
            # MUSIC
            #self.music.unload()
            #self.music.stop()
            self.media=vlc.Media(self.playlist[index])
            self.music.set_media(self.media)
            #self.music.load(self.playlist[index])
            self.music.play()
            #self.STATE = PlayerState.PLAYING
            self.playlist_index = index

            # CHANGE INFO
            cover_image = self.get_album_cover()
            self.cover_art_frame.cover_art_label.configure(
                require_redraw=True, image=cover_image, fg_color="#121212"
            )

            self.control_bar.set_music_title(   # truncates longer titles
                self.get_song_title(),
                self.get_song_artist(),
            )
            self.control_bar.update_play_button()

            self.bottom_frame.start_progress_bar(
                self.get_song_length(self.playlist[index]),
            )
            logging.info(
                "playing %s", self.get_song_title()
            )
            

        except Exception as e:
            logging.exception(e)

    def play_next_song(self, _event=None):
        if not self.playlist:
            return

        # PLAY FROM BEGINING
        if self.playlist_index >= len(self.playlist) - 1:
            self.playlist_index = 0
        else:
            self.playlist_index += 1
        self.load_and_play_song(self.playlist_index)

        # UPDATE SELECTION
        self.playlist_frame.song_list.selection_clear(0, tk.END)
        self.playlist_frame.song_list.select_set(self.playlist_index)
        logging.info("playing next song")

    def get_song_length(self, file_path):
        '''audio = File(file_path)
        if audio is not None and audio.info is not None:
            return audio.info.length
        return 0'''
        return self.music.get_length()

    def get_song_title(self):
        try:
            if self.media.is_parsed():
                return self.media.get_meta(0)
            else:
                self.media.parse()
                return self.media.get_meta(0)
        except Exception as e:
            logging.exception(e)
            return ""

        

    def get_album_cover(self):
        """if not file_path.endswith(".mp3"):
            return
        try:
            audio_file = id3.ID3(file_path)
            cover_data = None

            # APIC TAG FOR IMAGE DATA
            for tag in audio_file.getall("APIC"):
                if tag.mime in ("image/jpeg", "image/png"):
                    cover_data = tag.data
                    break
            if cover_data:
                # TEMP STORE COVER
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".jpg"
                ) as temp_file:
                    temp_file.write(cover_data)
                    temp_path = temp_file.name

                return ctk.CTkImage(
                    self.round_corners(Image.open(temp_path), 20),
                    size=(250, 250),
                )
            return
        except Exception as e:
            logging.error(e)
            return"""
         # gives the direct uri to cover jpg
        try:
            self.media.parse()
            print(self.media.get_meta(15))
            return ctk.CTkImage(
                self.round_corners(
                    Image.open(Path.from_uri(self.media.get_meta(15))),
                        20),
                size=(250,250)
            )
        except Exception as e:
            logging.exception(e)
            return
        return
        

    # ROUNDS ALBUM COVER
    def round_corners(self, image, radius):
        rounded_mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(rounded_mask)
        draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)

        rounded_image = Image.new("RGBA", image.size)
        rounded_image.paste(image, (0, 0), mask=rounded_mask)

        return rounded_image

    def get_song_artist(self):
        try:
            if self.media.is_parsed():
                return self.media.get_meta(1)
            else:
                self.media.parse()
                return self.media.get_meta(1)
        except exception as e:
            logging.exception(e)
            return ""

    def get_song_position(self):
        return self.music.get_position()

    def initialize_vlc(self):
        #pygame.init()
        #pygame.mixer.init()
        self.vlc_instance=vlc.Instance()
        self.music=vlc.MediaPlayer()
        
        #self.music = pygame.mixer.music

        # CREATE USEREVENT WHEN MUSIC ENDS
        #pygame.mixer.music.set_endevent(pygame.USEREVENT)

    # AUTOPLAY NEXT SONG AFTER SONG ENDS
    def check_for_events(self):
        #pygame.display.init()
        #for event in pygame.event.get():
         #   if event.type == pygame.USEREVENT:
          #      self.play_next_song()
        print(self.music.get_state())
        #if self.music.get_state() == vlc.State.Ended:
         #   self.play_next_song()

    def setup_icons(self):
        self.play_icon = ctk.CTkImage(Image.open("yami/data/play_arrow.png"))
        self.pause_icon = ctk.CTkImage(Image.open("yami/data/pause.png"))
        self.prev_icon = ctk.CTkImage(Image.open("yami/data/skip_prev.png"))
        self.next_icon = ctk.CTkImage(Image.open("yami/data/skip_next.png"))
        self.folder_icon = ctk.CTkImage(Image.open("yami/data/folder.png"))
        self.music_icon = ctk.CTkImage(Image.open("yami/data/music.png"))
        logging.info("icons setup")

    def setup_bindings(self):
        self.bind("<F10>", self.play_next_song)
        self.bind("<F8>", self.control_bar.play_previous)
        self.bind("<F9>", self.control_bar.play_pause)
        self.bind("<space>", self.control_bar.play_pause)

    def update_loop(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        self.after(1000, self.update_loop)


if __name__ == "__main__":
    music_player = MusicPlayer()
    music_player.mainloop()
