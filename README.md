<div align="center">

![yami-logo](.assets/vector/default-monochrome-black.svg)
---
![Static Badge](https://img.shields.io/badge/pip_install-yami--music--player-purple)
![Static Badge](https://img.shields.io/badge/Language-Python-red)
![GitHub last commit](https://img.shields.io/github/last-commit/DevER-M/yami)

<h3>
<code>yami</code> | An open-source music player with simple UI
</h3>

<p align="center">
Download or play music locally without ads!   
</p>

[Installation](#installation) • [Usage](#usage) • [Features](#features) • [Testing](#testing) • [Contributing](#contributing) • [License](#license)
</div>


## 🛠️ Getting Started

### Prerequisites
- **Python** 3.8+
- **pip** for dependency management

### Installation
#### From Pip
```sh
pip install yami-music-player
```
#### From Github
##### 1. Clone the Repository
```sh
git clone https://github.com/DevER-M/yami.git
cd yami
```
##### 2. Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install `yami-music-player` (in editable mode):
```sh
pip install -e .
```



# Usage

To run `yami`, use the following command in your terminal:

```sh
$ yami 
# Or
$ python -m yami
```

## Features

- **Spotdl Integration:** Download music directly from the app using spotdl
  - **Asynchronous Downloading :** From synchronous `spotdl.Downloader.search_and_download()`
- **Player Controls:**
  - **<img src="data/pause.png" alt="drawing" width="30" style="vertical-align:bottom"> :** Pause/play music
  - **<img src="data/skip_next.png" alt="drawing" width="30" style="vertical-align:bottom"> :** Play next song
  - **<img src="data/skip_prev.png" alt="drawing" width="30" style="vertical-align:bottom"> :** Play previous song
  - **<img src="data/folder.png" alt="drawing" width="30" style="vertical-align:bottom"> :** Choose folder
  - **<img src="data/music.png" alt="drawing" width="30" style="vertical-align:bottom"> :** Download music
  - **`ctrl+o` :** Choose folder

This will open the app, for the logs check the terminal.







## Screenshot
![pic](https://raw.githubusercontent.com/DevER-M/yami/refs/heads/for-pypi/.assets/pic.png)

