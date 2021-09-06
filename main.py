import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

window_height = 300
window_width = 400

canvas = tk.Tk()
canvas.geometry("400x300")
canvas.title("OCR Tool")
canvas.iconbitmap('images/icon.ico')
canvas.configure(bg='gray')
canvas.resizable(False, False)
screen_width = canvas.winfo_screenwidth()
screen_height = canvas.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
canvas.geometry("{}x{}+{}+{}".format(window_width,
                                     window_height, x_coordinate, y_coordinate))

canvas.filename = ""


def transcript_generator(input_path, target_format):
    if input_path == "":
        return

    output_path = os.path.splitext(input_path)[0] + "_OCR" + target_format
    image = cv2.imread(input_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hImg, wImg, _ = image.shape
    boxes = pytesseract.image_to_data(image)

    for x, box in enumerate(boxes.splitlines()):
        if x != 0:
            box = box.split()
            if len(box) == 12:
                x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
                cv2.rectangle(image, (x, y), (w + x, h + y), (0, 0, 255), 2)
                cv2.putText(image, box[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
                with open(output_path + '_Transcript.txt', 'a+') as f:
                    f.write(box[11] + " ")

    cv2.imwrite(output_path, image)
    cv2.imshow('OCR Result', image)
    cv2.waitKey(0)
    messagebox.showinfo(
        "Information", "File Transcript Generation Successful! Output placed in source folder")


def open_directory():
    canvas.filename = filedialog.askopenfilename(initialdir="C:/Users/Infinity/Documents", title="Select A File",
                                                 filetypes=(("Image Files", "*.png *.jpeg *.jpg *.bmp *.pgm"),
                                                            ("All Files", "*.*")))
    transcript_generator(canvas.filename, '.jpg')


browse_button = tk.Button(canvas, text="Browse File",
                          command=open_directory, font=("SAN_SERIF", 20, "bold")).pack(pady=100)

canvas.mainloop()
