#Imports for GUI
import tkinter as tk
from tkinter import filedialog, colorchooser
import threading
import os
#Needed for spectrogram color map preview
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

"""
GUI Logic, first goal is being able to select and audio file,
next goal is being able to check spectrogram generation
finally, being able to select config variables like window height
width, etc.

"""


class music_visualizer_gui:
    def __init__(self, visualizer_callback):

        """Some tk conventions I was unfamiliar with:
        root is the main window
        geometry is the size of the window in width x height format
        pady is padding in the y direction, padx is padding in the x direction
        pack is a geometry manager that organizes widgets in blocks before placing them in the parent widget
        frame is a container widget that can hold other widgets

        That's what I couldn't immediately intuit looking at boilerplate code.
        """

        self.root = tk.Tk()
        self.root.title("Music Visualizer Config")
        self.root.geometry("500x500")
        self.visualizer_callback = visualizer_callback

        #initialize config variables
        self.config = {
            "audio_file": None,
            "spec_output_name": tk.StringVar(value=""),
            "show_spectrogram": tk.BooleanVar(value=False),
            "color_map": tk.StringVar(value="magma"),
            "bar_color_low": "#FF00FF",
            "bar_color_high": "#FFFF00"
        }
        self.btn_file = tk.Button(self.root, text="Choose Audio File", command=self.choose_file)
        self.btn_file.pack(pady=5)
        self.lbl_file = tk.Label(self.root, text="No file selected")
        self.lbl_file.pack(pady=5)

        #Create a frame for color selector buttons (vertical layout)
        color_frame = tk.Frame(self.root)
        color_frame.pack(pady=10)

        #Low decibel color row
        low_row = tk.Frame(color_frame)
        low_row.pack(fill=tk.X, pady=2)
        self.btn_color_low = tk.Button(low_row, text="Choose Low Decibel Bar Color", command=self.choose_color_low)
        self.btn_color_low.pack(side=tk.LEFT, padx=5)
        self.lbl_color_low = tk.Label(low_row, text=self.config["bar_color_low"], width=12)
        self.lbl_color_low.pack(side=tk.LEFT, padx=5)
        self.lbl_color_low.config(bg=self.config["bar_color_low"])

        #High decibel color row
        high_row = tk.Frame(color_frame)
        high_row.pack(fill=tk.X, pady=2)
        self.btn_color_high = tk.Button(high_row, text="Choose High Decibel Bar Color", command=self.choose_color_high)
        self.btn_color_high.pack(side=tk.LEFT, padx=5)
        self.lbl_color_high = tk.Label(high_row, text=self.config["bar_color_high"], width=12)
        self.lbl_color_high.pack(side=tk.LEFT, padx=5)
        self.lbl_color_high.config(bg=self.config["bar_color_high"])

        #Set High Decibel Bar Color Same as Low button below the color selectors
        self.btn_color_same = tk.Button(color_frame, text="Use Single Color", command=self.choose_color_same)
        self.btn_color_same.pack(pady=5)

        
        #Checkbox for spectrogram generation
        self.chk_spectrogram = tk.Checkbutton(self.root, text="Generate Spectrogram (Note: Runs Before Visualizer)", variable=self.config["show_spectrogram"])
        self.chk_spectrogram.pack(pady=5)

        #Selection for spectrogram color map and custom color map creation
        #default color map options:
        self.available_color_maps = ["magma", "viridis", "plasma", "inferno", "cividis", "hot", "cool"]
        color_map_frame = tk.Frame(self.root)
        color_map_frame.pack(pady=5)
        tk.Label(color_map_frame, text="Spectrogram Color Map:").pack(side=tk.LEFT, padx=5)
        self.colormap_var = tk.StringVar(value=self.config["color_map"].get())
        #The *self.available_color_maps unpacks the list into individual arguments for the option menu
        self.color_map_menu = tk.OptionMenu(color_map_frame, self.colormap_var, *self.available_color_maps, command=self.update_colormap)
        #Removes the annoying little box which indicates this is a dropdown
        self.color_map_menu.config(indicatoron=0)
        self.color_map_menu.pack(side=tk.LEFT, padx=5)

        #Add a preview of the selected color map, so the user knows what it looks like.

        preview_frame = tk.Frame(self.root)
        preview_frame.pack(pady=5)
        tk.Label(preview_frame, text="Color Map Preview:").pack()

        #Create figure and canvas for preview
        self.preview_figure = Figure(figsize=(4, 0.5))
        self.preview_canvas = FigureCanvasTkAgg(self.preview_figure, master=preview_frame)
        self.preview_canvas.get_tk_widget().pack()

        #Initial preview
        self.update_colormap_preview(self.config["color_map"].get())

        btn_start = tk.Button(self.root, text="Start Visualizer", command=self.start_visualizer)
        btn_start.pack(pady=20)

        #status label
        self.lbl_status = tk.Label(self.root, text="", fg="black")
        self.lbl_status.pack(pady=5)

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
            filename = os.path.basename(file)
            self.config["spec_output_name"].set(filename.split('.')[0])
            self.lbl_file.config(text=filename)
    #function for choosing a color for the bars in the visualizer
    def choose_color_low(self):
        color = colorchooser.askcolor(title="Choose Bar Color")[1] 
        if color:
            self.config["bar_color_low"] = color
            self.lbl_color_low.config(bg=color)


    #function for choosing a color for the bars in the visualizer
    def choose_color_high(self):
        color = colorchooser.askcolor(title="Choose Bar Color")[1] 
        if color:
            self.config["bar_color_high"] = color
            self.lbl_color_high.config(bg=color)
    
    def choose_color_same(self):
        self.config["bar_color_high"] = self.config["bar_color_low"]
        self.lbl_color_high.config(bg=self.config["bar_color_high"])
    
    #function to update the color map preview
    def update_colormap_preview(self, cmap_name):
        self.preview_figure.clear()
        ax = self.preview_figure.add_subplot(111)
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        ax.set_xticks([])
        ax.set_yticks([])

        #display gradient
        ax.imshow(gradient, aspect='auto', cmap=cmap_name)
        self.preview_figure.tight_layout(pad=0)
        self.preview_canvas.draw()

    #function to update the color map
    def update_colormap(self, value):
        self.config["color_map"].set(value)
        self.update_colormap_preview(value)

    #function for displaying the status of the spectrogram generation
    def update_spectrogram_status(self, message, color):
        self.root.after(0, lambda: self.lbl_status.config(text=message, fg=color))


    #function to start the visualizer
    def start_visualizer(self):
        if self.visualizer_thread and self.visualizer_thread.is_alive():
            self.lbl_status.config(text="Visualizer is already running.", fg="red")
            return
        if not self.config["audio_file"]:
            self.lbl_status.config(text="Please select an audio file first.", fg="red")
            return
        if (self.config["show_spectrogram"].get()):
            self.lbl_status.config(text="Generating spectrogram...", fg="blue")
        else:
            self.lbl_status.config(text="Starting visualizer...", fg="blue")
        self.visualizer_thread = threading.Thread(target=self.visualizer_callback, args=(self,), daemon=True)
        self.visualizer_thread.start()
        self.check_visualizer_thread()
    #function to check if the visualizer thread is still running
    def check_visualizer_thread(self):
        if self.visualizer_thread.is_alive():
            self.root.after(500, self.check_visualizer_thread)
        else:
            self.lbl_status.config(text="Visualizer finished.", fg="green")
    