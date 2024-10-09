"""Entry point"""

import logging
from mus.music import MusicPlayer


logging.getLogger().setLevel(logging.INFO)

app = MusicPlayer()
app.mainloop()
