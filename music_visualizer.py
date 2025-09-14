import pygame as pg
from pygame import draw
import librosa
import numpy as np
import sys

#Imports for computing a spectrogram
import matplotlib.pyplot as plt
import librosa.display


#Define config variables
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
NUM_BARS = 80
SMOOTHING_FACTOR = 0.3
FPS = 60
AUDIO_FILE = "../music/SmashFull.mp3"
OUTPUT_SPECTROGRAM_FILE = "spectrogram.png"

# Load and play audio asynchronously with librosa
signal, sr = librosa.load(AUDIO_FILE, sr=None, mono=True)
#take an absolute valuef the short-time fourier transform of the signal
s = np.abs(librosa.stft(signal, n_fft=2048, hop_length=512))

#convert to decibels
s_db = librosa.amplitude_to_db(s, ref=np.max)

#Since librosa outputs negative dB values, need to shift them over so the quiestest parts are 0 dB
s_db = s_db - s_db.min()

#plot spectrogram and save to disk
plt.figure(figsize=(10, 6))
#Creates a spectrogram with a maagma color map
#Need to reverse the color map so that louder parts are brighter
librosa.display.specshow(s_db, sr=sr, x_axis='time', y_axis='log', cmap='magma')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.tight_layout()


plt.savefig(OUTPUT_SPECTROGRAM_FILE)
plt.close()

signal = (signal * 32767).astype(np.int16)  # Convert to int16 for pygame

# Initialize Pygame mixer and play audio
pg.mixer.init(frequency=sr)
sound = pg.mixer.Sound(AUDIO_FILE)
sound.play()

#Initialize Pygame display
pg.init()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Music Visualizer")
clock = pg.time.Clock()

chunk_size = len(signal) // (NUM_BARS * 1000)
bar_heights_prev = np.zeros(NUM_BARS)

running = True
frame_index=0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    #clear screen
    screen.fill((0, 0, 0))

    #get frome for fft
    start = frame_index
    end = frame_index + chunk_size
    if end > len(signal):
        break #end of song

    frame = signal[start:end]
    fft = np.fft.fft(frame)
    mag= np.abs(fft[:NUM_BARS])
    max_mag = np.max(mag)
    if max_mag == 0:
        mag = np.zeros_like(mag)
    else:
        mag = mag / max_mag  # Normalize magnitudes

    #smooth bar heights
    bar_heights = SMOOTHING_FACTOR * mag + (1 - SMOOTHING_FACTOR) * bar_heights_prev
    bar_heights_prev = bar_heights
    bar_heights_pixels = (bar_heights * WINDOW_HEIGHT).astype(int)

    #draw bars
    bar_width = WINDOW_WIDTH / NUM_BARS
    for i, h in enumerate(bar_heights_pixels):
        x = int(i * bar_width)
        y = WINDOW_HEIGHT - h
        color = (int(255 * bar_heights[i]), 50, 255 - int(255 * bar_heights[i])) #color gradient
        draw.rect(screen, color, (x,y,int(bar_width*0.8) ,h))
    pg.display.flip()
    clock.tick(FPS)
    frame_index += chunk_size
pg.quit()
sys.exit()