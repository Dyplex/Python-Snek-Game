import tkinter as tk
import vlc

# Create a tkinter window
window = tk.Tk()

# Create a vlc media player
player = vlc.MediaPlayer("testvideo.mp4")

# Play the video
player.play()



# Start the tkinter event loop
window.mainloop()

# Remaining code goes here
print("Video has finished playing.")
