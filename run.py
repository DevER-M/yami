from mus.music import MusicPlayer
import asyncio

loop = asyncio.get_event_loop()
app = MusicPlayer(loop)
app.mainloop()
