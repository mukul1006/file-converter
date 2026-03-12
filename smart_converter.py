import os
from tkinter import *
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

from PIL import Image
from pdf2docx import Converter
from docx2pdf import convert
from moviepy import VideoFileClip
from pydub import AudioSegment


# ---------------- FILE CONVERSION FUNCTIONS ---------------- #

def convert_file(file_path, output_format):

    try:
        name, ext = os.path.splitext(file_path)
        ext = ext.lower()

        output_file = name + "." + output_format

        # IMAGE CONVERSION
        if ext in [".png", ".jpg", ".jpeg", ".bmp"]:

            img = Image.open(file_path)

            if output_format in ["jpg", "jpeg"]:
                img.convert("RGB").save(output_file)

            else:
                img.save(output_file)

        # PDF -> DOCX
        elif ext == ".pdf" and output_format == "docx":

            cv = Converter(file_path)
            cv.convert(output_file)
            cv.close()

        # DOCX -> PDF
        elif ext == ".docx" and output_format == "pdf":

            convert(file_path, output_file)

        # VIDEO -> AUDIO
        elif ext in [".mp4", ".mov", ".avi"] and output_format == "mp3":

            video = VideoFileClip(file_path)
            video.audio.write_audiofile(output_file)

        # AUDIO CONVERSION
        elif ext in [".wav", ".mp3"]:

            audio = AudioSegment.from_file(file_path)
            audio.export(output_file, format=output_format)

        else:
            messagebox.showerror("Error", "Conversion not supported")
            return

        messagebox.showinfo("Success", f"File converted to {output_format}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- DRAG & DROP ---------------- #

def drop(event):
    file_path = event.data.strip("{}")
    file_entry.delete(0, END)
    file_entry.insert(0, file_path)


# ---------------- FILE BROWSER ---------------- #

def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, END)
    file_entry.insert(0, file_path)


# ---------------- CONVERT BUTTON ---------------- #

def start_conversion():

    file_path = file_entry.get()
    output_format = format_entry.get()

    if not file_path or not output_format:
        messagebox.showerror("Error", "Please select file and format")
        return

    convert_file(file_path, output_format)


# ---------------- GUI ---------------- #

root = TkinterDnD.Tk()
root.title("Smart Universal File Converter")
root.geometry("500x300")

Label(root, text="Smart Universal File Converter", font=("Arial", 16)).pack(pady=10)

file_entry = Entry(root, width=50)
file_entry.pack(pady=10)

file_entry.drop_target_register(DND_FILES)
file_entry.dnd_bind('<<Drop>>', drop)

Button(root, text="Browse File", command=browse_file).pack()

Label(root, text="Convert To (example: pdf, jpg, mp3)").pack(pady=10)

format_entry = Entry(root)
format_entry.pack()

Button(root, text="Convert File", command=start_conversion, bg="green", fg="white").pack(pady=20)

root.mainloop()