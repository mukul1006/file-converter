import subprocess
import os
from pdf2docx import Converter
from docx2pdf import convert

def convert_file(input_file, output_format):

    name, ext = os.path.splitext(input_file)
    ext = ext.lower()

    output_file = name + "." + output_format

    try:

        # PDF → DOCX
        if ext == ".pdf" and output_format == "docx":

            cv = Converter(input_file)
            cv.convert(output_file)
            cv.close()

        # DOCX → PDF
        elif ext == ".docx" and output_format == "pdf":

            convert(input_file, output_file)

        # Other formats via FFmpeg
        else:

            command = [
                "ffmpeg",
                "-y",
                "-i",
                input_file,
                output_file
            ]

            subprocess.run(command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

    except Exception as e:
        print("Conversion error:", e)

    return output_file