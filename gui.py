#Imports for GUI
import tkinter as tk
from tkinter import filedialog, colorchooser
import threading

"""
GUI Logic, first goal is being able to select and audio file,
next goal is being able to check spectrogram generation
finally, being able to select config variables like window height
width, etc.

"""


class music_visualizer_gui:
    def __init__(self, visualizer_callback):
        self.root = tk.Tk()
        self.root.title("Music Visualizer Config")
        self.root.geometry("400x400")
        self.visualizer_callback = visualizer_callback

        #initialize config variables
        self.config = {
            "audio_file": None,
            "show_spectrogram": tk.BooleanVar(value=True),
            "color_map": tk.StringVar(value="magma"),
            "bar_color": "#FF00FF"
        }
        self.btn_file = tk.Button(self.root, text="Choose Audio File", command=self.choose_file)
        self.btn_file.pack(pady=5)
        self.lbl_file = tk.Label(self.root, text="No file selected")
        self.lbl_file.pack(pady=5)

        self.lbl_status = tk.Label(self.root, text="", fg="black")
        self.lbl_status.pack(pady=5)


        self.chk_spectrogram = tk.Checkbutton(self.root, text="Generate Spectrogram", variable=self.config["show_spectrogram"])
        self.chk_spectrogram.pack(pady=5)

        self.btn_color = tk.Button(self.root, text="Choose Bar Color", command=self.choose_color)
        self.btn_color.pack(pady=5)
        self.lbl_color = tk.Label(self.root, text=self.config["bar_color"])
        self.lbl_color.pack(pady=5)
        
        btn_start = tk.Button(self.root, text="Start Visualizer", command=self.start_visualizer)
        btn_start.pack(pady=20)
        self.visualizer_thread = None


    def run(self):
        self.root.mainloop()

    #function for selecting an audio file
    def choose_file(self):
        file = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg")])
        if file:
            self.config["audio_file"] = file
            self.lbl_file.config(text=file)
    #fucntion for choosing a color for the bars in the visualizer
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Bar Color")[1] 
        if color:
            self.config["bar_color"] = color
            self.lbl_color.config(bg=color)
    #function to start the visualizer

    def start_visualizer(self):
        if self.visualizer_thread and self.visualizer_thread.is_alive():
            self.lbl_status.config(text="Visualizer is already running.", fg="red")
            return
        if not self.config["audio_file"]:
            self.lbl_status.config(text="Please select an audio file first.", fg="red")
            return
        self.lbl_status.config(text="Starting visualizer...", fg="green")
        self.visualizer_thread = threading.Thread(target=self.visualizer_callback, args=(self,), daemon=True)
        self.visualizer_thread.start()
        self.check_visualizer_thread()

    def check_visualizer_thread(self):
        if self.visualizer_thread.is_alive():
            self.root.after(500, self.check_visualizer_thread)
        else:
            self.lbl_status.config(text="Visualizer finished.", fg="blue")
    