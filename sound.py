# import tkinter
from tkinter import ttk
import tkinter as tk
import vlc
import os


class SoundBox:
    def __init__(
        self,
        parent_frame,
        filepath,
        parent_list,
        col=0,
        row=0,
        volume=None,
        repeat=None,
        reorganize_callback=None,
    ):
        self.filepath = filepath
        self.column = col
        self.row = row
        self.parent_list = parent_list

        self.reorganize_callback = reorganize_callback

        self.instance = vlc.Instance()

        self.media = self.instance.media_new(self.filepath)
        self.media.parse()

        self.total_duration = self.media.get_duration()
        self.total_duration_sec = self.total_duration / 1000
        self.file_name = os.path.basename(filepath)

        self.sound = self.instance.media_player_new()
        self.sound.set_media(self.media)

        # Tkinger widgets start here
        self.box = tk.Frame(parent_frame, bd=2, relief="groove")
        self.box.grid(
            column=self.column, row=self.row, columnspan=None, padx=10, pady=5
        )

        # separator = ttk.Separator(self.box, orient="horizontal")
        # separator.grid(row=0, column=0, columnspan=4, sticky="ew", pady=5)

        self.sound_name = ttk.Label(
            self.box, text=self.file_name, wraplength=350, justify="left"
        )
        self.sound_name.grid(row=0, column=0, rowspan=None, columnspan=4, sticky="nsew")

        self.play_button = tk.Button(
            self.box,
            text="Play",
            command=self.play_sound,
            width=10,
        )
        self.play_button.grid(row=1, column=0, sticky="ew")
        self.default_bg = self.play_button.cget("bg")
        self.default_fg = self.play_button.cget("fg")
        self.default_active_bg = self.play_button.cget("activebackground")
        self.default_active_fg = self.play_button.cget("activeforeground")
        self.play_button.config(
            bg="darkgreen",
            fg="white",
            activebackground="green",
            activeforeground="white",
        )

        self.stop_button = tk.Button(
            self.box,
            text="Stop",
            command=self.stop_sound,
            width=10,
        )
        self.stop_button.grid(row=1, column=1, sticky="ew")

        style = ttk.Style()
        style.configure("Thick.Horizontal.TProgressbar", thickness=10)
        self.progress_bar = ttk.Progressbar(
            self.box,
            orient="horizontal",
            length=100,
            mode="determinate",
            style="Thick.Horizontal.TProgressbar",
        )
        self.progress_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.playing_time_text = ttk.Label(
            self.box, text=f"000.00 / {self.total_duration_sec:.2f}", anchor="e"
        )
        self.playing_time_text.grid(row=3, column=0)

        self.repeat_var = tk.BooleanVar(value=False)
        self.repeat_tick = ttk.Checkbutton(
            self.box, text="Repeat", variable=self.repeat_var
        )
        self.repeat_tick.grid(row=3, column=1)

        self.volume_var = tk.IntVar(value=100)
        self.volume_bar = tk.Scale(
            self.box,
            from_=100,
            to=0,
            orient="vertical",
            variable=self.volume_var,
            command=self.apply_volume,
        )
        self.volume_bar.grid(row=1, column=2, rowspan=3)

        self.movement_buttons_frame = ttk.Frame(self.box)
        self.movement_buttons_frame.grid(row=0, column=4, rowspan=4)

        self.move_up_button = tk.Button(
            self.movement_buttons_frame,
            text="^",
            command=lambda: reorganize_callback(self, self.parent_list, "up"),
        )
        self.move_up_button.grid(row=0, column=0)

        self.move_down_button = tk.Button(
            self.movement_buttons_frame,
            text="v",
            command=lambda: reorganize_callback(self, self.parent_list, "down"),
        )
        self.move_down_button.grid(row=1, column=0)

        self.move_left_button = tk.Button(
            self.movement_buttons_frame,
            text="<",
            command=lambda: reorganize_callback(self, self.parent_list, "left"),
        )
        self.move_left_button.grid(row=2, column=0)

        self.move_right_button = tk.Button(
            self.movement_buttons_frame,
            text=">",
            command=lambda: reorganize_callback(self, self.parent_list, "right"),
        )
        self.move_right_button.grid(row=3, column=0)

        self.delete_button = tk.Button(
            self.movement_buttons_frame, text="X", fg="red", command=self.delete_self
        )
        self.delete_button.grid(row=4, column=0)

        if volume is not None:
            self.apply_volume(volume)
            self.volume_bar.set(volume)
        else:
            self.apply_volume(100)  # test this

        if repeat is not None:
            self.repeat_var.set(value=repeat)

    def play_sound(self):
        # set initial volume
        self.apply_volume(self.volume_var.get())

        if self.sound.get_state() == vlc.State.Ended:
            self.sound.stop()

        self.sound.play()
        self.play_button.config(
            bg=self.default_bg,
            fg=self.default_fg,
            activebackground=self.default_active_bg,
            activeforeground=self.default_active_fg,
        )
        self.stop_button.config(
            bg="darkred", fg="white", activebackground="red", activeforeground="white"
        )

        # delay start
        self.box.after(100, self.update_progress)

    def stop_sound(self):
        self.repeat_var.set(0)
        self.sound.stop()
        self.play_button.config(
            bg="darkgreen",
            fg="white",
            activebackground="green",
            activeforeground="white",
        )
        self.stop_button.config(
            bg=self.default_bg,
            fg=self.default_fg,
            activebackground=self.default_active_bg,
            activeforeground=self.default_active_fg,
        )

    def pause_sound(self):
        self.sound.pause()

    def update_progress(self):
        current = self.sound.get_time()

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
            self.play_button.config(text="Pause", command=self.pause_sound)
        elif state == vlc.State.Paused:
            self.box.after(100, self.update_progress)
            self.play_button.config(text="Play", command=self.play_sound)
        else:
            self.progress_bar["value"] = 0
            self.play_button.config(text="Play", command=self.play_sound)
            if self.repeat_var.get():
                self.play_sound()

    def apply_volume(self, value):
        if self.sound.get_state() != vlc.State.NothingSpecial:
            self.sound.audio_set_volume(int(float(value)))

    def get_filepath(self):
        return self.filepath

    def delete_self(self):
        # Stop VLC
        if self.sound:
            self.sound.stop()
            self.sound.release()
            self.sound = None

        # Destroy GUI
        if self.box:
            self.box.destroy()
            self.box = None

        # Remove from parent list
        if hasattr(self, "parent_list") and self in self.parent_list:
            self.parent_list.remove(self)

        for i, box in enumerate(self.parent_list):
            box.row = i
            box.box.grid(row=i)
