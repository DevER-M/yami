"""Console entry point"""

import logging
from yami.music import MusicPlayer

"""add sys args and logs"""

logging.getLogger().setLevel(logging.INFO)

app = MusicPlayer()
app.mainloop()
