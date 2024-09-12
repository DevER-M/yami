from mus.music import MusicPlayer
from asyncio import new_event_loop

loop = new_event_loop()
app = MusicPlayer(loop)
app.mainloop()
