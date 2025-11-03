import vlc

media = vlc.Media(
    r"/Users/mith/Music/Music/Media.localized/Music/The Avalanches/Since I Left You (20th Anniversary Deluxe Edition)/1-05 Avalanche Rock.m4a"
)
player = vlc.MediaPlayer()
player.set_media(media)
inst: vlc.Instance = player.get_instance()
player.play()
import time

time.sleep(0.5)
print(media.get_meta(1))
print(media.get_meta(0))


print(media.get_meta(15))
while player.is_playing():
    time.sleep(0.5)
