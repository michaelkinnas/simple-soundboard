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
        sound_box = SoundBox(containter, file_path, col=0, row=len(boxes) + 2)
        boxes.append(sound_box)


def add_sound_process(container, boxes):
    file_path = get_file()
    add_sound(container, file_path, boxes)


def save_layout():
    pass


def load_layout():
    pass


def stop_all():
    pass


def pause_all(boxes):
    for item in boxes:
        item.pause_sound()


def main():
    boxes = []
    # make sound var whatever sound you want to play

    root = Tk()
    root.title("The most amazingest sound board in the known universe")
    root.resizable(False, False)

    # container = ttk.Frame(root, padding=10)
    # container.grid(column=0, row=0)

    # toolbar
    add_button = ttk.Button(
        root, command=lambda: add_sound_process(root, boxes), text="Add sound"
    )
    add_button.grid(column=0, row=0)

    save_layout_button = ttk.Button(
        root, command=lambda: save_layout(), text="Save configuration"
    )
    save_layout_button.grid(column=1, row=0)

    load_layout_button = ttk.Button(
        root, command=lambda: load_layout(), text="Load configuration"
    )
    load_layout_button.grid(column=2, row=0)

    second_row_frame = ttk.Frame(padding=10)
    second_row_frame.grid(column=0, row=1, columnspan=3)

    pause_all_button = ttk.Button(
        second_row_frame, command=lambda: pause_all(boxes), text="Pause all"
    )
    pause_all_button.grid(column=0, row=1)

    stop_all_button = ttk.Button(
        second_row_frame, command=lambda: stop_all(boxes), text="Stop all"
    )
    stop_all_button.grid(column=1, row=1)

    root.mainloop()


if __name__ == "__main__":
    main()
