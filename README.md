# Python Music Visualizer

A music visualizer written in Python with a simple GUI. Users can modify the visualizer's colors, and choose to output spectrograms of the audio files they've selected.

## How to run

### With EXE

Available at this link: https://uofi.box.com/s/vuk1ip8h0dhfsp5vcsyurpp392v4hm31

Run the MusicVisualizer.exe. Note that this version a little slow to boot up (you'll be greeted with a blank terminal for a bit) and generate spectrograms. The spectrograms output to the same folder the exe is in.

### From the command line

Ensure you have the necessary dependencies

- Pygame (for the visualizer itself)
- Librosa (for loading and handling audio files)
- Matplotlib (for spectrogram generation)
- Numpy (for gradient calculations)

Navigate to the repository in your terminal of choice and run main.py, a GUI should pop up asking you to select an audio file and various other configs for the script. Currently, only .mp3 and .wav files have been tested, but it will additionally recognize .ogg and .flac files.

Once you've selected a file, you can choose the bar colors, whether or not you want a spectrogram (if you do, it'll be outputted in the same folder as main.py as "spectrogram.png"). Click start visualizer and the script will begin running. Note: if you selected generate spectrogram, there will be a delay before the visualizer pops up.