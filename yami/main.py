"""Console entry point"""

import logging
from yami.music import MusicPlayer

"""add sys args and logs"""

logging.getLogger().setLevel(logging.INFO)
def entry():
    app = MusicPlayer()
    app.mainloop()

if __name__=="__main__":
    entry()
