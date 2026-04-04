# import tkinter
from tkinter import ttk
import tkinter as tk
import vlc
import os


class SoundBox:
    def __init__(self, parent_frame, filepath, col=0, row=0):
        self.filepath = filepath
        self.instance = vlc.Instance()

        self.media = self.instance.media_new(self.filepath)
        self.media.parse()

        self.total_duration = self.media.get_duration()
        self.total_duration_sec = self.total_duration / 1000
        self.file_name = os.path.basename(filepath)

        self.sound = self.instance.media_player_new()
        self.sound.set_media(self.media)

        self.column = col
        self.row = row

        self.box = ttk.Frame(parent_frame, padding=6)
        self.box.grid(column=self.column, row=self.row, columnspan=3)

        self.sound_name = ttk.Label(self.box, text=self.file_name, width=35)
        self.sound_name.grid(column=0, row=0, columnspan=3)
        # self.song_name.pack()

        # self.play_button = ttk.Button(
        #     self.box, text="Play", command=self.play_sound, width=15
        # )
        self.play_button = tk.Button(
            self.box,
            text="Play",
            bg="darkgreen",
            fg="white",
            activebackground="green",
            activeforeground="white",
            command=self.play_sound,
            width=10,
            # height=1,
        )
        self.play_button.grid(column=0, row=1)
        # self.play_button.pack()
        # self.play_button.place(x=100, y=100)

        self.stop_button = tk.Button(
            self.box,
            text="Stop",
            bg="darkred",
            fg="white",
            activebackground="red",
            activeforeground="white",
            command=self.stop_sound,
            width=10,
        )
        self.stop_button.grid(column=1, row=1)
        # self.stop_button.pack()

        self.progress_bar = ttk.Progressbar(
            self.box, orient="horizontal", length=268, mode="determinate"
        )
        self.progress_bar.grid(column=0, row=2, pady=5, columnspan=2)
        # self.progress_bar.pack()

        self.playing_time_text = ttk.Label(
            self.box, text=f"000.00 / {self.total_duration_sec:.2f}", anchor="e"
        )
        self.playing_time_text.grid(column=0, row=3)
        # self.playing_time_text.pack()

        self.repeat_var = tk.BooleanVar(value=False)
        self.repeat_tick = ttk.Checkbutton(
            self.box, text="Repeat", variable=self.repeat_var
        )
        self.repeat_tick.grid(column=1, row=3)
        # self.repeat_tick.pack()

        self.volume_var = tk.IntVar(value=100)
        self.volume_bar = tk.Scale(
            self.box,
            from_=100,
            to=0,
            orient="vertical",
            variable=self.volume_var,
            command=self.apply_volume,
        )
        self.volume_bar.grid(column=2, row=1, rowspan=3)

    def play_sound(self):
        # set initial volume
        self.apply_volume(self.volume_var.get())

        if self.sound.get_state() == vlc.State.Ended:
            self.sound.stop()

        self.sound.play()

        # self.update_progress()
        self.box.after(100, self.update_progress)  # delay start

    def stop_sound(self):
        self.repeat_var.set(0)
        self.sound.stop()

    def pause_sound(self):
        self.sound.pause()

    def update_progress(self):
        current = self.sound.get_time()
        # total = self.sound.get_length()

        current_readable = max(0, current / 1000)

        self.playing_time_text["text"] = (
            f"{current_readable:06.2f} / {self.total_duration_sec:.2f}"
        )

        if self.total_duration > 0:
            percent = (current / self.total_duration) * 100
            self.progress_bar["value"] = percent

        state = self.sound.get_state()

        if state == vlc.State.Playing:
            self.box.after(100, self.update_progress)
            self.play_button.config(text="Pause")
            self.play_button.config(command=self.pause_sound)

        elif state == vlc.State.Paused:
            self.box.after(100, self.update_progress)
            self.play_button.config(text="Play")
            self.play_button.config(command=self.play_sound)
        else:
            self.progress_bar["value"] = 0
            self.play_button.config(text="Play")
            self.play_button.config(command=self.play_sound)
            if self.repeat_var.get():
                self.play_sound()

    def apply_volume(self, value):
        if self.sound.get_state() != vlc.State.NothingSpecial:
            self.sound.audio_set_volume(int(float(value)))
