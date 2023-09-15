import tkinter as tk

# create a tkinter window
window = tk.Tk()
window.title("Main Menu")

# set the window size
window.geometry("800x600")

# set up the font
font = ("Arial", 48)

# create a play button
play_button = tk.Button(window, text="Play", font=font, bg="green", fg="white", width=10, height=5)

# place the play button in the center of the window
play_button.place(relx=0.5, rely=0.5, anchor="center")

# function to handle button click
def play_game():
    print("Play button clicked")

# set the command for the play button to call the play_game function
play_button.configure(command=play_game)

# start the tkinter event loop
window.mainloop()