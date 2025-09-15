import gui
import music_visualizer

if __name__ == "__main__":
    gui = gui.music_visualizer_gui(music_visualizer.run_visualizer)
    gui.run()