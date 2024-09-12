from mus.music import MusicPlayer
from asyncio import new_event_loop,run

loop = new_event_loop()
app = MusicPlayer(loop)
run(app.mainloop())
