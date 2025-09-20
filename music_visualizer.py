import pygame as pg
from pygame import draw
import librosa
import numpy as np
import sys

import matplotlib
#this is here so matplotlib doesn't mess with tk or pygame.
#Allows matplotlib to only write to files
matplotlib.use('Agg')
#Imports for computing a spectrogram
import matplotlib.pyplot as plt
import librosa.display

#Writes spectrogram to file
def generate_spectrogram(s_db, sr, color_map, output_file, gui_object):
        try:
            #we'll just update the status label directly in the gui instead of here
            #gui_object.lbl_status.config(text="Generating spectrogram...", fg="blue")
            #plot spectrogram and save to disk
            plt.figure(figsize=(10, 6))
            #Creates a spectrogram with a whatever is the selected color map
            #Need to reverse the color map so that louder parts are brighter
            librosa.display.specshow(s_db, sr=sr, x_axis='time', y_axis='log', cmap=color_map)
            plt.colorbar(format='%+2.0f dB')
            plt.title(f'{gui_object.config["spec_output_name"].get()} Spectrogram')
            plt.tight_layout()
            #Get the name of the file for naming the spectrogram image
            plt.savefig(output_file)
            plt.close()
            gui_object.lbl_status.config(text=f"Spectrogram saved to {output_file}", fg="green")
            return True
        except Exception as e:
            gui_object.lbl_status.config(text=f"Error generating spectrogram: {e}", fg="red")
            return False


def run_visualizer(gui_object):
    #Define config variables
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    NUM_BARS = 80
    BAR_COLOR_LOW = gui_object.config["bar_color_low"]
    BAR_COLOR_HIGH = gui_object.config["bar_color_high"]
    SPECTROGRAM_COLOR = gui_object.config["color_map"].get()
    SMOOTHING_FACTOR = 0.3
    FPS = 60
    AUDIO_FILE = gui_object.config["audio_file"]
    OUTPUT_SPECTROGRAM_FILE = f"{gui_object.config['spec_output_name'].get()}_spectrogram.png"

    # Load and play audio asynchronously with librosa
    signal, sr = librosa.load(AUDIO_FILE, sr=None, mono=True)
    #take an absolute valuef the short-time fourier transform of the signal
    s = np.abs(librosa.stft(signal, n_fft=2048, hop_length=512))

    #convert to decibels
    s_db = librosa.amplitude_to_db(s, ref=np.max)

    #Since librosa outputs negative dB values, need to shift them over so the quiestest parts are 0 dB
    s_db = s_db - s_db.min()
    if gui_object.config["show_spectrogram"].get():
        result = generate_spectrogram(s_db, sr, SPECTROGRAM_COLOR, OUTPUT_SPECTROGRAM_FILE, gui_object)
        if not result:
            #Spectrogram failed, exit so the error message stays up
            return
        gui_object.lbl_status.config(text="Starting visualizer...", fg="blue")

    signal = (signal * 32767).astype(np.int16)  # Convert to int16 for pygame


    # Initialize Pygame mixer and play audio
    pg.mixer.init(frequency=sr)
    pg.mixer.music.load(AUDIO_FILE)
    pg.mixer.music.play()

    #Initialize Pygame display
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption("Music Visualizer")
    clock = pg.time.Clock()

    #Note there's an error that will be thrown if the audio file is too short, but it doesn't crash the program
    #And the spectrogram works properly still, so there isn't a reason to refactor for it.
    chunk_size = len(signal) // (NUM_BARS * 1000)
    bar_heights_prev = np.zeros(NUM_BARS)

    running = True
    frame_index=0

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Check if music is still playing or we've reached the end of the signal
        if not pg.mixer.music.get_busy() or frame_index >= len(signal):
            running = False
            break

        #clear screen
        screen.fill((0, 0, 0))

        #get frame for fft
        start = frame_index
        end = frame_index + chunk_size
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
            color = interpolate_color(BAR_COLOR_LOW, BAR_COLOR_HIGH, bar_heights[i])
            draw.rect(screen, color, (x,y,int(bar_width*0.8) ,h))
        pg.display.flip()
        clock.tick(FPS)
        frame_index += chunk_size

    pg.quit()

#Interpolate between two colors between 0 and 1 (where 0 is no decibels and 1 is the maximum decibel level)
def interpolate_color(color1, color2, t):
    # color1 and color2 are hex strings, t is between 0 and 1
    c1 = tuple(int(color1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    c2 = tuple(int(color2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    return tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))