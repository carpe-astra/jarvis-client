from collections import deque

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from listener.audio import AudioManager

audio_listener = AudioManager()

xs = deque(maxlen=50)
ys = deque(maxlen=50)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


def animate(i):
    audio_listener.read_buffer()
    xs.append(i)
    ys.append(audio_listener.energy)

    ax.clear()
    ax.plot(xs, ys)
    ax.set_ylim(0, 1)


ani = animation.FuncAnimation(fig, animate, interval=17)
plt.show()
