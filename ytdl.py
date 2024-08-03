import yt_dlp
import sounddevice as sd
import numpy as np
from scipy.io import wavfile

def play_wav(file_path):
    sample_rate, audio_data = wavfile.read(file_path)
    audio_data = audio_data.astype(np.float32) / 32768.0  # Normalize to float32 format
    sd.play(audio_data, samplerate=sample_rate)
    sd.wait()  # Wait until the file has finished playing


query=input("enter song name: ")

ydl_opts = {
    'format': 'wav/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
     ydl.extract_info(f"{query}")