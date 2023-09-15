import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
import os

# Define the countdown timer function
def countdown():
    global time_left
    if time_left > 0:
        # Update the time left label
        time_left_label.config(text="Time left: " + str(time_left))

        # Check if it's time to display an image
        if time_left == 55:
            image_path = os.path.join("assets", "judgements", "S.png")
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo
            
        elif time_left == 30:
            image_path = os.path.join("assets", "judgements", "A.png")
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo
        elif time_left == 25:
            image_path = os.path.join("assets", "judgements", "B.png")
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo
        elif time_left == 20:
            image_path = os.path.join("assets", "judgements", "C.png")
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo
        elif time_left == 15:
            image_path = os.path.join("assets", "judgements", "D.png")
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo

        # Schedule the next update
        root.after(1000, countdown)
        # Decrement the time left
        time_left -= 1
    else:
        # Update the time left label
        time_left_label.config(text="Time's up!")
        

# Define the function to handle food collection
def collect_food():
    global time_left
    time_left += 10
    # Update the time left label
    time_left_label.config(text="Time left: " + str(time_left))
    # Check if it's time to display an image
    if time_left >= 30:
        image_path = os.path.join("assets", "judgements", "S.png")
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

# Create the main window
root = tk.Tk()

# Create the time left label
time_left = 10
time_left_label = tk.Label(root, text="Time left: " + str(time_left))
time_left_label.pack()

# Create the image label with a default image
default_image_path = os.path.join("assets", "judgements", "yousuc.png")
default_image = Image.open(default_image_path)
default_photo = ImageTk.PhotoImage(default_image)
label = tk.Label(root, image=default_photo)
label.pack()

# Create the food button
food_button = tk.Button(root, text="Collect food", command=collect_food)
food_button.pack()

gif_image_path = os.path.join("assets", "livereactions", "livesnekrecotn1.gif")
gif_image = Image.open(gif_image_path)
gif_photo = ImageTk.PhotoImage(gif_image)
lbl = ImageLabel(root, image=gif_photo)

# Start the countdown timer
countdown()

lbl = ImageLabel(root)
lbl.load('assets/livereactions/livesnekrecotn1.gif')
lbl.pack(side="right", anchor="nw")

# Run the main loop
root.mainloop()
