from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from sound import SoundBox
import pickle


def get_file():
    file_path = filedialog.askopenfilename(
        title="Select a sound file",
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")],
    )
    return file_path


def add_sound(container, file_path, boxes, volume=None, repeat=None):
    if file_path:
        sound_box = SoundBox(
            container,
            file_path,
            boxes,
            col=0,
            row=len(boxes) + 2,
            # col=len(boxes),
            # row=0,
            volume=volume,
            repeat=repeat,
        )
        boxes.append(sound_box)


def add_sound_process(container, boxes):
    file_path = get_file()
    add_sound(container, file_path, boxes)


def save_layout(boxes):
    sounds = []
    for soundbox in boxes:
        settings = {
            "file_path": soundbox.get_filepath() + "\n",
            "volume": soundbox.volume_var.get(),
            "repeat": soundbox.repeat_var.get(),
        }
        print(settings)
        sounds.append(settings)

    file_path = filedialog.asksaveasfilename(
        title="Save file as...",
        filetypes=[("All files", "*")],
    )

    if file_path:
        with open(file_path, "wb") as f:
            pickle.dump(sounds, f)


def load_layout(container, boxes):
    file_path = filedialog.askopenfilename(
        title="Select a sound list file",
        filetypes=[("All files", "*")],
    )

    if file_path:
        with open(file_path, "rb") as f:
            loaded_data = pickle.load(f)

        for sound in loaded_data:
            add_sound(
                container=container,
                file_path=sound["file_path"].strip(),
                boxes=boxes,
                volume=sound["volume"],
                repeat=sound["repeat"],
            )


def stop_all(boxes):
    for item in boxes:
        item.stop_sound()


def pause_all(boxes):
    for item in boxes:
        item.pause_sound()


def on_frame_configure(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


def main():
    boxes = []

    root = Tk()
    root.title("sssoundboard")
    # root.resizable(False, True)
    root.grid_rowconfigure(2, weight=1)  # row 2 grows vertically
    root.grid_columnconfigure(0, weight=1)  # canvas column grows horizontally

    top_toolbar = ttk.Frame(root)
    top_toolbar.grid(
        row=0,
        column=0,
    )
    top_toolbar.grid_columnconfigure(0, weight=1)
    top_toolbar.grid_columnconfigure(1, weight=1)
    top_toolbar.grid_columnconfigure(2, weight=1)

    # toolbar
    add_button = ttk.Button(
        top_toolbar,
        command=lambda: add_sound_process(container=scrollable_frame, boxes=boxes),
        text="Add sound",
    )
    add_button.grid(column=0, row=0, sticky="ew")

    save_layout_button = ttk.Button(
        top_toolbar, command=lambda: save_layout(boxes=boxes), text="Save list"
    )
    save_layout_button.grid(column=1, row=0, sticky="ew")

    load_layout_button = ttk.Button(
        top_toolbar,
        command=lambda: load_layout(container=root, boxes=boxes),
        text="Load list",
    )
    load_layout_button.grid(column=2, row=0, sticky="ew")

    middle_toolbar = ttk.Frame()
    middle_toolbar.grid(column=0, row=1, pady=5)
    middle_toolbar.grid_columnconfigure(0, weight=1)
    middle_toolbar.grid_columnconfigure(1, weight=1)

    pause_all_button = ttk.Button(
        middle_toolbar, command=lambda: pause_all(boxes), text="Pause all"
    )
    pause_all_button.grid(column=0, row=0, sticky="ew")

    stop_all_button = ttk.Button(
        middle_toolbar, command=lambda: stop_all(boxes), text="Stop all"
    )
    stop_all_button.grid(column=1, row=0, sticky="ew")

    canvas = tk.Canvas(root)
    canvas.grid(row=2, column=0, sticky="nsew")

    vert_scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    vert_scrollbar.grid(row=2, column=1, sticky="ns")
    canvas.configure(yscrollcommand=vert_scrollbar.set)

    hor_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    hor_scrollbar.grid(row=3, column=0, sticky="ew")
    canvas.configure(xscrollcommand=hor_scrollbar.set)

    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>", func=lambda event: on_frame_configure(event, canvas)
    )

    root.mainloop()


if __name__ == "__main__":
    main()
