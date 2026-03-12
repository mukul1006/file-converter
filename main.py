import customtkinter as ctk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import threading
import os
import cv2

from converter import convert_file

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

files = []

app = TkinterDnD.Tk()
app.geometry("1000x650")
app.title("Smart Universal File Converter")


# SIDEBAR
sidebar = ctk.CTkFrame(app, width=220)
sidebar.pack(side="left", fill="y")

title = ctk.CTkLabel(sidebar, text="Smart Converter", font=("Arial",22))
title.pack(pady=20)

formats = [
"mp3","wav","aac",
"mp4","mkv","avi",
"png","jpg","jpeg",
"webp","bmp","gif",
"pdf","docx"
]

format_box = ctk.CTkComboBox(sidebar, values=formats)
format_box.set("Select Format")
format_box.pack(pady=10)


# ADD FILE BUTTON
def add_files():

    selected = filedialog.askopenfilenames()

    for f in selected:

        files.append(f)

        file_list.insert("end", f"{os.path.basename(f)}\n")

add_file_btn = ctk.CTkButton(
sidebar,
text="Add Files",
command=add_files
)

add_file_btn.pack(pady=10)


# ADD FOLDER BUTTON
def add_folder():

    folder = filedialog.askdirectory()

    for f in os.listdir(folder):

        path = os.path.join(folder,f)

        if os.path.isfile(path):

            files.append(path)

            file_list.insert("end", f"{f}\n")

folder_btn = ctk.CTkButton(
sidebar,
text="Add Folder",
command=add_folder
)

folder_btn.pack(pady=10)


# MAIN AREA
main = ctk.CTkFrame(app)
main.pack(fill="both", expand=True, padx=20, pady=20)


drop_box = ctk.CTkLabel(
main,
text="Drag & Drop Files Here",
height=120
)

drop_box.pack(fill="x", pady=10)


file_list = ctk.CTkTextbox(main, height=200)
file_list.pack(fill="x", pady=10)


progress = ctk.CTkProgressBar(main)
progress.set(0)
progress.pack(fill="x", pady=10)


status = ctk.CTkLabel(main, text="")
status.pack(pady=5)


# DRAG DROP
def drop(event):

    paths = app.tk.splitlist(event.data)

    for p in paths:

        files.append(p)

        file_list.insert("end", f"{os.path.basename(p)}\n")

drop_box.drop_target_register(DND_FILES)
drop_box.dnd_bind("<<Drop>>", drop)


# CONVERSION
def convert_thread():

    fmt = format_box.get()

    if fmt == "Select Format":
        status.configure(text="Select format first")
        return

    total = len(files)

    for i,f in enumerate(files):

        convert_file(f, fmt)

        progress.set((i+1)/total)

        status.configure(text=f"Converted {i+1}/{total}")

    status.configure(text="Conversion Complete")


def start_convert():

    threading.Thread(target=convert_thread).start()


convert_btn = ctk.CTkButton(
main,
text="Convert Files",
height=45,
command=start_convert
)

convert_btn.pack(pady=20)


app.mainloop()