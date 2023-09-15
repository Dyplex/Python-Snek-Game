import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()

# Set the window title
root.title("GIF Example")

# Load the GIF image
gif = Image.open("liveD.gif")
gif_frames = []
try:
    while True:
        gif_frames.append(gif.copy())
        gif.seek(len(gif_frames))  # Move to the next frame
except EOFError:  # End of frames
    pass

# Define a function to update the label with the GIF
def update_label():
    global remaining_label, remaining, gif_label, gif_frame, gif_frames
    
    # Check the remaining value
    if remaining < 10:
        # Show the GIF
        gif_label.pack(side="left")
        remaining_label.pack_forget()
        
        # Update the GIF frame
        gif_frame += 1
        if gif_frame >= len(gif_frames):
            gif_frame = 0
        gif_image = ImageTk.PhotoImage(gif_frames[gif_frame])
        gif_label.configure(image=gif_image)
        gif_label.image = gif_image
        
    else:
        # Show the remaining value
        remaining_label.configure(text="Remaining: {}".format(remaining))
        remaining_label.pack(side="left")
        gif_label.pack_forget()

# Define the remaining value
remaining = 5

# Create the label for the remaining value
remaining_label = ttk.Label(root, text="Remaining: {}".format(remaining))

# Create the label for the GIF
gif_frame = 0
gif_image = ImageTk.PhotoImage(gif_frames[gif_frame])
gif_label = ttk.Label(root, image=gif_image)

# Add the labels to the window
remaining_label.pack(side="left")
gif_label.pack_forget()

# Set up the update function to be called every second
root.after(1000, update_label)

# Start the main loop
root.mainloop()
