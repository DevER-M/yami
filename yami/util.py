from enum import Enum

SUPPORTED_FORMATS = (".mp3", ".ogg", ".wav", ".m4a", ".opus")
BUTTON_WIDTH = 10
GEOMETRY = "800x500"
TITLE = "Music Player"
EVENT_INTERVAL = 100


class PlayerState(Enum):
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3


def make_time_string(song_position, song_length):
    curtime = song_position * song_length

    cur_minutes = int(curtime // 60)
    cur_seconds = int(curtime % 60)

    song_min = int(song_length // 60)
    song_sec = int(song_length % 60)

    return f"{cur_minutes:02d}:{cur_seconds:02d} / {song_min:02d}:{song_sec:02d}"
