"""Main script for deploying the listener."""

from audio import AudioManager

from listener.config import settings

audio_listener = AudioManager()

while True:
    audio_listener.read_buffer()
    print(f"{audio_listener.energy:.4f}", end="\r")
