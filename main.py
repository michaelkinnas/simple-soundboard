from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from sound import SoundBox
import pickle


# TODO: For the future refactor to cleaner code
def reorganize_soundboxes(current_box, boxes, command="up"):
    boxes_in_column = [box for box in boxes if box.column == current_box.column]
    if command == "up":
        if len(boxes_in_column) == 1:
            return

        if current_box.row == 0:
            return

        for box in boxes_in_column:
            if box.row == current_box.row - 1:
                box.row += 1

        current_box.row -= 1

    if command == "down":
        if current_box.row == len(boxes_in_column) - 1:
            return

        for box in boxes_in_column:
            if box.row == current_box.row + 1:
                box.row -= 1

        current_box.row += 1

    if command == "right":
        if len(boxes_in_column) == 1:
            return

        boxes_in_next_column = [
            box for box in boxes if box.column == current_box.column + 1
        ]

        # get last row in next column
        if len(boxes_in_next_column) == 0:
            next_available_row = 0
        else:
            next_available_row = max(boxes_in_next_column, key=lambda x: x.row).row + 1

        # move boxes below that sound up
        for box in boxes_in_column:
            if box.row > current_box.row:
                box.row -= 1

        current_box.row = next_available_row
        current_box.column += 1

    if command == "left":
        # if it's the first column don't move
        if current_box.column == 0:
            return

        boxes_in_next_column = [
            box for box in boxes if box.column == current_box.column - 1
        ]

        boxes_in_right_column = [
            box for box in boxes if box.column == current_box.column + 1
        ]

        # get last row in next column
        if len(boxes_in_next_column) == 0:
            next_available_row = 0
        else:
            next_available_row = max(boxes_in_next_column, key=lambda x: x.row).row + 1

        # move boxes below that box up
        for box in boxes_in_column:
            if box.row > current_box.row:
                box.row -= 1

        # if column is left empty move boxes in right column left
        if len(boxes_in_column) == 1:
            for box in boxes_in_right_column:
                box.column -= 1

        current_box.row = next_available_row
        current_box.column -= 1

    # reposition widgets in the parent grid
    for box in boxes:
        box.box.grid(row=box.row, column=box.column)


def get_file():
    file_path = filedialog.askopenfilename(
        title="Select a sound file",
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")],
    )
    return file_path


def add_sound(
    container, file_path, boxes, volume=None, repeat=None, row=None, column=None
):
    if file_path:
        sound_box = SoundBox(
            container,
            file_path,
            boxes,
            col=0 if column is None else column,
            row=len(boxes) if row is None else row,
            # col=len(boxes),
            # row=0,
            volume=volume,
            repeat=repeat,
            reorganize_callback=reorganize_soundboxes,
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
            "row": soundbox.row,
            "column": soundbox.column,
        }
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
                row=sound["row"],
                column=sound["column"],
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
        command=lambda: load_layout(container=scrollable_frame, boxes=boxes),
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
