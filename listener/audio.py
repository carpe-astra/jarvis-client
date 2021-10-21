"""Class for handling microphone audio buffers"""

from collections import deque

import numpy as np
import pyaudio


class AudioManager:
    def __init__(
        self,
        format: int = pyaudio.paInt16,
        channels: int = 1,
        rate: int = 16000,
        input: bool = True,
        frames_per_buffer: int = 1024,
        sample_buffer_length: int = 8,
    ):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.input = input
        self.frames_per_buffer = frames_per_buffer

        self.format_normal = 1.0 / 2 ** (2 * self.format - 1)
        self.sample_buffer_queue = deque(maxlen=sample_buffer_length)

        self.energy: float = 0

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=self.input,
            frames_per_buffer=self.frames_per_buffer,
        )

    def _update_energy(self):
        sum_squares = 0.0
        count = len(self.sample_buffer_queue) * len(self.sample_buffer_queue[0])

        for buffer in self.sample_buffer_queue:
            for sample in buffer:
                level = sample * self.format_normal
                sum_squares += level ** 2

        self.energy = np.sqrt(sum_squares / count)

    def update_sample_buffer(self, data):
        self.sample_buffer_queue.appendleft(data)
        self._update_energy()

    def read_buffer(self):
        data = np.fromstring(self.stream.read(self.frames_per_buffer), dtype=np.int16)
        self.update_sample_buffer(data)
        return data
