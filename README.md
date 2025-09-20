# Python Music Visualizer

A music visualizer written in Python with a simple GUI. Users can modify the visualizer's colors, and choose to output spectrograms of the audio files they've selected.

## How to run

Ensure you have the necessary dependencies

- Pygame (for the visualizer itself)
- Librosa (for loading and handling audio files)
- Matplotlib (for spectrogram generation)
- Numpy (for gradient calculations)

Navigate to the repository in your command terminal of choice and run main.py, a GUI should pop up asking you to select an audio file and various other configs for the script. Currently, only .mp3 and .wav files have been tested, but it will additionally recognize .ogg and .flac files.

Once you've selected a file, you can choose the bar colors, whether or not you want a spectrogram (if you do, it'll be outputted in the same folder as main.py as "spectrogram.png"). Click start visualizer and the script will begin running. Note: if you selected generate spectrogram, there will be a delay before the visualizer pops up.

## Plans for the future

Currently, it's a pretty complete package, but I have some QOL and feature improvements I want to add to really flesh out this project. Here's some basic ideas I have:

- Currently working on allowing users to select a color map for the generated spectrogram. I personally think magma is perfect for the visualization, but it should be the user's choice.
- Use a seperate thread for the matplotlib spectrogram feature, so there is not a significant delay before the visualizer appears.
- Allow the user to adjust the pygame window for the visualizer.