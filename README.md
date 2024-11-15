<div align="center">

![yami-logo](https://github.com/DevER-M/yami/blob/main/.assets/vector/default-monochrome-black.svg?raw=true)
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

[Installation](#installation) • [Usage](#usage) • [Features](#features) • [Contributing](#contributing) • [License](#license)
</div>

## 🔍Overview
`Yami` is a lightweight, open-source music player built in Python. It focuses on simplicity and ease of use, providing an intuitive user interface (UI) for users to manage and play their music. Whether you're playing local files or downloading from online sources using spotdl, Yami offers a seamless experience. This project is designed for users who want a minimalistic, cross-platform music player with the ability to integrate external sources like Spotify/Youtube Music.

## 📸Screenshot
<div align="center">
<img align="center" src="https://github.com/DevER-M/yami/blob/main/.assets/pic.png?raw=true">
<img align="center" src="https://github.com/DevER-M/yami/blob/main/.assets/example.gif?raw=true">
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
  - **<img src="https://github.com/DevER-M/yami/blob/main/data/pause.png?raw=true" alt="drawing" width="30" style="vertical-align:bottom"> :** Pause/play music
  - **<img src="https://github.com/DevER-M/yami/blob/main/data/skip_next.png?raw=true" alt="drawing" width="30" style="vertical-align:bottom"> :** Play next song
  - **<img src="https://github.com/DevER-M/yami/blob/main/data/skip_prev.png?raw=true" alt="drawing" width="30" style="vertical-align:bottom"> :** Play previous song
  - **<img src="https://github.com/DevER-M/yami/blob/main/data/folder.png?raw=true" alt="drawing" width="30" style="vertical-align:bottom"> :** Choose folder
  - **<img src="https://github.com/DevER-M/yami/blob/main/data/music.png?raw=true" alt="drawing" width="30" style="vertical-align:bottom"> :** Download music
  - **`ctrl+o` :** Choose folder

This will open the app, for the logs check the terminal.

# Contributing

Contributions are welcome and greatly appreciated! Here's how you can contribute:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

# License

Distributed under the GPLV3 License. See [`LICENSE`](LICENSE) for more information.


# Credits
- [Custom Tkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Spotdl](https://github.com/spotDL/spotify-downloader)
- [@ElSaico](https://github.com/ElSaico) for fixing [locale scaling](https://github.com/ElSaico/CustomTkinter/tree/fix-locale-scaling)

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=DevER-M/yami&type=Date)](https://star-history.com/#iamDyeus/tkreload&Date)





