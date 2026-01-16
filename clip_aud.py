import librosa
import soundfile as sf

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os

audio_file_path = None
output_dir = None

def browse_files():
    global audio_file_path

    audio_file_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select a File",
        filetypes=(("Audio files", "*.mp3"), ("All files", "*.*"))
    )

    if audio_file_path:
        selected_label.config(text=os.path.basename(audio_file_path))
        status_label.config(text="", fg="green")


def output_path():
    global output_dir

    output_dir = filedialog.askdirectory(
        initialdir=os.getcwd(),
        title="Select Output Directory"
    )

    if output_dir:
        output_label.config(text=output_dir)
        status_label.config(text="", fg="green")


import os
import soundfile as sf

def say_hello():
    if not audio_file_path:
        status_label.config(text="Please select a file first!", fg="red")
        return

    if not output_dir:
        status_label.config(text="Please select an output directory!", fg="red")
        return

    try:
        duration = int(entry_name.get())
    except ValueError:
        status_label.config(text="Invalid duration!", fg="red")
        return

    status_label.config(text="Generating...", fg="blue")
    progress_bar["value"] = 0
    root.update_idletasks()

    file_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    
    with sf.SoundFile(audio_file_path, mode='r') as f:
        sr = f.samplerate
        channels = f.channels
        chunk_samples = int(duration * sr)

        total_chunks = (len(f) + chunk_samples - 1) // chunk_samples
        progress_bar["maximum"] = total_chunks

        chunk_index = 1

        while True:
            try:
                chunk = f.read(
                    frames=chunk_samples,
                    dtype="float32",
                    always_2d=True
                )
            except sf.LibsndfileError:
                break  # clean exit at EOF

            if chunk.size == 0:
                break

            output_file = os.path.join(
                output_dir, f"{file_name}_chunk_{chunk_index}.wav"
            )

            sf.write(output_file, chunk, sr)

            progress_bar["value"] = chunk_index
            root.update_idletasks()

            chunk_index += 1

    status_label.config(text="Generated!", fg="green")


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Simple audio clip app")
root.geometry("320x420")

browse_button = tk.Button(root, text="Browse Files", command=browse_files)
browse_button.pack(pady=10)

selected_label = tk.Label(root, text="No file selected", wraplength=280)
selected_label.pack()

output_dir_button = tk.Button(root, text="Select Output Directory", command=output_path)
output_dir_button.pack(pady=10)

output_label = tk.Label(root, text="No output directory selected", wraplength=280)
output_label.pack()

label_name = tk.Label(root, text="Enter clip interval (seconds):")
label_name.pack(pady=10)

entry_name = tk.Entry(root, width=20)
entry_name.pack(pady=5)

button_hello = tk.Button(root, text="Generate", command=say_hello)
button_hello.pack(pady=10)

progress_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=250,
    mode="determinate"
)
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()
