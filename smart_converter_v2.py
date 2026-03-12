import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from pdf2docx import Converter
from docx2pdf import convert
from moviepy import VideoFileClip
from pydub import AudioSegment

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Universal File Converter")
app.geometry("600x420")

selected_file = ""


def browse_file():
    global selected_file
    file = filedialog.askopenfilename()
    selected_file = file
    file_label.configure(text=file)


def convert_file():

    if selected_file == "":
        status_label.configure(text="Please select a file")
        return

    name, ext = os.path.splitext(selected_file)
    ext = ext.lower()
    output_format = format_entry.get()

    output_file = name + "." + output_format

    progress.start()

    try:

        # IMAGE
        if ext in [".png", ".jpg", ".jpeg", ".bmp"]:

            img = Image.open(selected_file)

            if output_format in ["jpg", "jpeg"]:
                img.convert("RGB").save(output_file)
            else:
                img.save(output_file)

        # PDF -> DOCX
        elif ext == ".pdf" and output_format == "docx":

            cv = Converter(selected_file)
            cv.convert(output_file)
            cv.close()

        # DOCX -> PDF
        elif ext == ".docx" and output_format == "pdf":

            convert(selected_file, output_file)

        # VIDEO -> AUDIO
        elif ext in [".mp4", ".mov", ".avi"] and output_format == "mp3":

            video = VideoFileClip(selected_file)
            video.audio.write_audiofile(output_file)

        # AUDIO
        elif ext in [".wav", ".mp3"]:

            audio = AudioSegment.from_file(selected_file)
            audio.export(output_file, format=output_format)

        status_label.configure(text="Conversion Complete!")

    except Exception as e:
        status_label.configure(text=str(e))

    progress.stop()


title = ctk.CTkLabel(app, text="Smart Universal File Converter", font=("Arial", 24))
title.pack(pady=20)

browse_btn = ctk.CTkButton(app, text="Select File", command=browse_file)
browse_btn.pack(pady=10)

file_label = ctk.CTkLabel(app, text="No file selected")
file_label.pack(pady=5)

format_entry = ctk.CTkEntry(app, placeholder_text="Enter output format (pdf, jpg, mp3...)")
format_entry.pack(pady=15)

convert_btn = ctk.CTkButton(app, text="Convert File", command=convert_file)
convert_btn.pack(pady=10)

progress = ctk.CTkProgressBar(app)
progress.pack(pady=20)
progress.set(0)

status_label = ctk.CTkLabel(app, text="")
status_label.pack()

app.mainloop()