import tkinter as tk
import snekbkup

def start_game():

    snekbkup.start_game()

# create a tkinter window
window = tk.Tk()
window.title("Main Menu")

# create a button that starts the game
button = tk.Button(window, text="Play Game", command=start_game)
button.pack()

# start the tkinter event loop
window.mainloop()
