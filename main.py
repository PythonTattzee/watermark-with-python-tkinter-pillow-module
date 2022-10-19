import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageDraw, ImageFont
import urllib.request
from urllib.request import urlopen
from io import BytesIO

window = tk.Tk()
window.title("Watermark your image")
window.geometry("900x600")
window.title('show image')

canvas = Canvas(window, width=900, height=600)
canvas.pack(fill="both", expand=True)

label = canvas.create_text(450, 20, text='Add Photo to page', font=('courier', 18, 'bold'))
watermark_text_label = canvas.create_text(450, 40, text='Type-in the watermark text', font=('courier', 15, 'bold'))
watermark_text = tk.Entry(canvas)
watermark_input = canvas.create_window(450, 60, window=watermark_text)

def open_image():
    global pillow_img
    global filename
    global font
    global im
    truetype_url = 'https://github.com/google/fonts/blob/main/ofl/courierprime/CourierPrime-Regular.ttf?raw=true'
    font = ImageFont.truetype(urlopen(truetype_url), size=65)

    # get a drawing context
    f_types = [('Jpg Files', '*.jpg')]
    filename = fd.askopenfilename(filetypes=f_types)
    pillow_img = Image.open(filename).convert("RGBA")

    # img = ImageTk.PhotoImage(pillow_img)
    # canvas.create_image(0, 120, anchor="nw", image=img)
    #canvas.create_text(220, 320, anchor="nw", text=watermark_text.get(), font=('courier', 35, 'normal'), fill="white")

    # create watermark on a file itself
    text_watermarked_img = ImageDraw.Draw(pillow_img)
    # draw text on top of the image as a watermark
    x = 0
    y = 0
    for i in range(10):
        for j in range(10):
            x += 100
            y += 100
            text_watermarked_img.text((x, y), watermark_text.get(), font=font, fill="white")

    # create image watermark
    watermark_image_url = "https://cdn-icons-png.flaticon.com/512/1393/1393392.png"
    u = urllib.request.urlopen(watermark_image_url)
    raw_data = u.read()
    u.close()
    im = Image.open(BytesIO(raw_data))
    im = im.resize((100, 100), Image.ANTIALIAS)
    text_watermarked_img.bitmap((0, 0), im, fill=None)
    w_img = ImageTk.PhotoImage(pillow_img)
    canvas.create_image(0, 0, anchor="nw", image=w_img)

    pillow_img.show()

def update_text():
    global pillow_img
    pillow_img = Image.open(filename).convert("RGBA")
    text_watermarked_img = ImageDraw.Draw(pillow_img)
    x = 0
    y = 0
    for i in range(10):
        for j in range(10):
            x += 100
            y += 100
            text_watermarked_img.text((x, y), watermark_text.get(), font=font, fill="white")
    text_watermarked_img.bitmap((0, 0), im, fill=None)
    w_img = ImageTk.PhotoImage(pillow_img)
    canvas.create_image(0, 0, anchor="nw", image=w_img)
    pillow_img.show()

def save():
    pillow_img.convert('RGBA')
    pillow_img.save('watermark.png')


open_button = Button(canvas, text='Open File', width=30, command=open_image)
save_button = Button(canvas, text='Save Watermarked File', width=30, command=save)
update_button = Button(canvas, text='Open File', width=30, command=update_text)
open_button_window = canvas.create_window(310, 100, window=open_button)
save_button_window = canvas.create_window(590, 100, window=save_button)
update_button_window = canvas.create_window(450, 150, window=update_button)

window.mainloop()
