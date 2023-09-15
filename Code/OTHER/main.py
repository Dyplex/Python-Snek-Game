import requests
from io import BytesIO
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk

root = tk.Tk()

# Load the GIF images from the URLs
gif_urls = {
    "S": "https://s12.gifyu.com/images/liveS.gif",
    "A": "https://s12.gifyu.com/images/liveA.gif",
    "B": "https://s12.gifyu.com/images/liveB.gif",
    "C": "https://s12.gifyu.com/images/liveC.gif",
    "D": "https://s12.gifyu.com/images/liveD.gif",
    "YOU SUCC": "https://s11.gifyu.com/images/liveSucc.gif",
    "Time's up!": "https://s11.gifyu.com/images/liveSucc.gif"
}

# Create a dictionary of GIF images from the URLs
gif_images = {}
for key, value in gif_urls.items():
    response = requests.get(value)
    gif_bytes = BytesIO(response.content)
    gif_image = Image.open(gif_bytes)
    frames = []
    for frame in ImageSequence.Iterator(gif_image):
        frames.append(frame.copy())
    photos = [ImageTk.PhotoImage(frame) for frame in frames]
    gif_images[key] = photos

# Create a label widget
label = tk.Label(root)
label.pack()

# Set initial values for variables
remaining = 55
previous_live = 0
puncte = 0

def livecounter(label, remaining):
    global puncte, previous_live

    if puncte > previous_live:
        print("Score increased!")
        remaining += 3
        previous_live = puncte

    if remaining <= 0:
        label.config(text="Time's up!")
        gif_key = "Time's up!"
    else:
        label.config(text="Time left: {}".format(remaining))
        remaining -= 1
        if remaining < 10:
            gif_key = "YOU SUCC"
            print("YOU SUCC")
        elif remaining < 15:
            gif_key = "D"
            print("D")
        elif remaining < 20:
            gif_key = "C"
            print("C")
        elif remaining < 25:
            gif_key = "B"
            print("B")
        elif remaining < 30:
            gif_key = "A"
            print("A")
        elif remaining < 55:
            gif_key = "S"
            print("S")
        else:
            return
    photo_idx = (60 - remaining) % len(gif_images[gif_key])
    photo = gif_images[gif_key][photo_idx]
    label.config(image=photo)
    label.image = photo
    label.after(1000, livecounter, label, remaining)

livecounter(label, remaining)

root.mainloop()
