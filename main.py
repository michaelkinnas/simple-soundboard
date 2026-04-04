from tkinter import *
from tkinter import ttk, filedialog
from sound import SoundBox


def get_file():
    file_path = filedialog.askopenfilename(
        title="Select a sound file",
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")],
    )
    return file_path


def add_sound(containter, file_path, boxes):
    if file_path:
        sound_box = SoundBox(containter, file_path, boxes, col=0, row=len(boxes) + 2)
        boxes.append(sound_box)


def add_sound_process(container, boxes):
    file_path = get_file()
    add_sound(container, file_path, boxes)


def save_layout(boxes):
    sound_file_paths = [x.get_filepath() + "\n" for x in boxes]

    file_path = filedialog.asksaveasfilename(
        title="Save file as...",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )

    if file_path:
        with open(file_path, "w") as f:
            f.writelines(sound_file_paths)


def load_layout(container, boxes):
    file_path = filedialog.askopenfilename(
        title="Select a sound list file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )

    if file_path:
        with open(file_path, "r") as f:
            file_paths = f.readlines()

    file_paths = [x.strip() for x in file_paths]

    for file_path in file_paths:
        add_sound(container, file_path, boxes)


def stop_all(boxes):
    for item in boxes:
        item.stop_sound()


def pause_all(boxes):
    for item in boxes:
        item.pause_sound()


def main():
    boxes = []

    root = Tk()
    root.title("The most amazingest sound board in the known universe")
    root.resizable(False, True)

    # toolbar
    add_button = ttk.Button(
        root,
        command=lambda: add_sound_process(container=root, boxes=boxes),
        text="Add sound",
    )
    add_button.grid(column=0, row=0, sticky="ew")

    save_layout_button = ttk.Button(
        root, command=lambda: save_layout(boxes=boxes), text="Save list"
    )
    save_layout_button.grid(column=1, row=0, sticky="ew")

    load_layout_button = ttk.Button(
        root, command=lambda: load_layout(container=root, boxes=boxes), text="Load list"
    )
    load_layout_button.grid(column=2, row=0, sticky="ew")

    second_row_frame = ttk.Frame()
    second_row_frame.grid(column=0, row=1, columnspan=3, padx=80, pady=5)

    pause_all_button = ttk.Button(
        second_row_frame, command=lambda: pause_all(boxes), text="Pause all"
    )
    pause_all_button.grid(column=0, row=1, sticky="ew")

    stop_all_button = ttk.Button(
        second_row_frame, command=lambda: stop_all(boxes), text="Stop all"
    )
    stop_all_button.grid(column=1, row=1, sticky="ew")

    root.mainloop()


if __name__ == "__main__":
    main()
