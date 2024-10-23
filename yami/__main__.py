"""Entry point"""

import logging
from yami.music import MusicPlayer


logging.getLogger().setLevel(logging.INFO)

app = MusicPlayer()
app.mainloop()
