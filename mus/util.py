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
