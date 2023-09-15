#TO DO LIST
#1. Add audio and game icon
#5. Add custom textures to the snake and board (maybe change textures when reaching a specific puncte)
#4. Add DMC puncte system
#3. Modify interface
"""
2. Add main menu (Settings, custom keybinds and volume slider)
6. Make it so that the game moves faster if you have more puncte
7. (Maybe) Clean the code
8. (Maybe) Add a neato shader to the gaem
"""
import requests
from io import BytesIO
import tkinter as tk
from tkinter import *
from itertools import count, cycle #necessary for GIFs to work
import os
import sys
import pygame #pygame because I couldn't think of a better way to add sound
import random
from pygame import mixer
import time
import cv2
from PIL import Image, ImageTk, ImageSequence
import threading

pygame.mixer.init()
background_song = pygame.mixer.Sound(r'C:\Users\User\Desktop\Python Snak gayum\sounds\background_noise.mp3')
eat_sound = pygame.mixer.Sound(r'C:\Users\User\Desktop\Python Snak gayum\sounds\munch.mp3')
gaemover_sound = pygame.mixer.Sound(r'C:\Users\User\Desktop\Python Snak gayum\sounds\gaemover.mp3')
testsound = pygame.mixer.Sound(r'C:\Users\User\Desktop\Python Snak gayum\assets\cutscene\cutscene_snd.mp3')
testsound.play(0)

#Setari joc
#=========================================
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
AREA_WIDTH = 500
AREA_HEIGHT = 500
SPEED = 200 #Viteza sarpe, cool idea, cu cat mai mult scor faci cu atat mai repede se misca sarpele
SPACE_SIZE = 50 #Cat de mare o sa fie pixelii
BODY_PARTS = 2 #cate bucati o sa aiba sarpele la inceput
SNEK_CULOARE = "#000000"
MANCARE_CULOARE = "#FF0000" #Remind me to make this a sprite not a solid color

#=========================================


class Sarpe:
   #Spawneaza sarpele
   def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNEK_CULOARE, tag="sarpe")
            self.squares.append(square)

class Mancare:
    #basically spawneaza random mancarea, that's it
    def __init__(self):

        x = random.randint(0, (AREA_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (AREA_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=MANCARE_CULOARE, tag="mancare")

def next_turn(sarpe, mancare):
    
    x, y = sarpe.coordinates[0] #coordonatele sarpelui, MUST be in englisj

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    sarpe.coordinates.insert(0, (x,y)) #tot ce face codul asta este sa adauge patratele la sarpe, gotta make a skin for it tho LATER
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNEK_CULOARE)
    sarpe.squares.insert(0, square)

    if x == mancare.coordinates[0] and y == mancare.coordinates[1]: #Functia care elimina mancarea si adauga la marimea sarpelui
        global puncte, previous_puncte, countdown_label, livecounter_label
        puncte += 1
        previous_puncte = 0
        
        #if puncte > previous_puncte:
            #print("Score increased!")
            

        label.config(text="Puncte: {}".format(puncte))
        canvas.delete("mancare")
        mancare = Mancare()
        eat_sound.play()
        
    else:
         del sarpe.coordinates[-1] #asta da iluzia ca sarpele nostru se misca
         canvas.delete(sarpe.squares[-1]) #de fapt de fiecare data cand apare un patrat in fata
         del sarpe.squares[-1]#patratul din spate este sters

    if coliziuni(sarpe):
        joc_terminat()

    else:
      fereastra.after(SPEED, next_turn, sarpe, mancare)

def change_direction(new_direction): #are legatura cu def next_turn(sarpe, mancare)
   
    global direction
    
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def coliziuni(sarpe):
    
    x, y = sarpe.coordinates[0]

    if x < 0 or x >= AREA_WIDTH:
        return True
    
    elif y < 0 or y >= AREA_WIDTH:
        return True
    
    for BODY_PARTS in sarpe.coordinates[1:]:
        if x == BODY_PARTS[0] and y == BODY_PARTS[1]:
            return True
    
    return False

def joc_terminat():
    gaemover_sound.play()
    background_song.stop()
    #canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('Sonic advanced 2',70), text="GAME OVER", fill="red", tag="gameover")
    
    pathtophoto = Image.open("assets/gaemover.png")
    image1 = ImageTk.PhotoImage(pathtophoto)
    panel1 = Label(fereastra, image=image1)
    panel1.image = image1 #keep a reference
    panel1.place(x=40, y=150)

# center the label in the window uhh just gonna... leave this here actually daca ii dau disable totul pare sa mearga??
    #label.place(relx=0.5, rely=0.5, anchor="center")

def countdown(label, remaining):
    global puncte, previous_puncte

    if puncte > previous_puncte:
        #print("Score increased!")
        remaining += 3
        previous_puncte = puncte

    if remaining <= 0:
        label.config(text="Time's up!")
        img = Image.open("assets/judgements/IMPROVED/rankSuccJud.png")
        #print("Time's up!")
    else:
        label.config(text="Time left: {}".format(remaining))
        remaining -= 1
        if remaining < 10:
            img = Image.open("assets/judgements/IMPROVED/rankSuccJud.png")
            #print("YOU SUCC")
        elif remaining < 15:
            img = Image.open("assets/judgements/IMPROVED/rankDjud.png")
            #print("D")
        elif remaining < 20:
            img = Image.open("assets/judgements/IMPROVED/rankCjud.png")
            #print("C")
        elif remaining < 25:
            img = Image.open("assets/judgements/IMPROVED/rankBjud.png")
            #print("B")
        elif remaining < 30:
            img = Image.open("assets/judgements/IMPROVED/rankAjud.png")
            #print("A")
        elif remaining < 55:
            img = Image.open("assets/judgements/IMPROVED/rankSjud.png")
            #print("S")
        else:
            return
        #img = img.resize((50, 50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo
        label.after(1000, countdown, label, remaining)

def livecounter(label, remaining):
    global puncte, previous_live

    if puncte > previous_live:
        #print("Score increased!")
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
            #print("YOU SUCC")
        elif remaining < 15:
            gif_key = "D"
            #print("D")
        elif remaining < 20:
            gif_key = "C"
            #print("C")
        elif remaining < 25:
            gif_key = "B"
            #print("B")
        elif remaining < 30:
            gif_key = "A"
            #print("A")
        elif remaining < 55:
            gif_key = "S"
        else:
            return
    photo_idx = (60 - remaining) % len(gif_images[gif_key])
    photo = gif_images[gif_key][photo_idx]
    label.config(image=photo)
    label.image = photo
    label.after(1000, livecounter, label, remaining)

#SETARI TEXT (puncte)
#=========================================
fereastra = tk.Tk()
fereastra.title("Snek gaem ඞ")
fereastra.iconbitmap('icon.ico')
fereastra.resizable(False, False)


#volosim opencv, aparent nu poate sa acceseze sonorul???? found a work around tho
cap = cv2.VideoCapture('assets/cutscene/cutscene_vid.mp4')
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
    cv2.imshow('Cutscene', frame)
    if cv2.waitKey(25) & 0xFF == ord(' '): #Apasa SPACE ca sa dai skip :p
        break
    cv2.resizeWindow('Cutscene', SCREEN_WIDTH, SCREEN_HEIGHT)
cap.release()
cv2.destroyAllWindows()

testsound.stop()
background_song.play(-1)

#remaining = 55
puncte = 0
previous_puncte = 0
previous_live = 0

direction = 'down' #Ah da asta are legatura cu def next_turn(sarpe, mancare), basically din ce directie vine sarpele

gif_urls = {
    "S": "https://s12.gifyu.com/images/liveS.gif",
    "A": "https://s12.gifyu.com/images/liveA.gif",
    "B": "https://s12.gifyu.com/images/liveB.gif",
    "C": "https://s12.gifyu.com/images/liveC.gif",
    "D": "https://s12.gifyu.com/images/liveD.gif",
    "YOU SUCC": "https://s11.gifyu.com/images/liveSucc.gif",
    "Time's up!": "https://s11.gifyu.com/images/liveSucc.gif"
}

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

# Asta pune pe ecran rankurile (S A B C D)
countdown_label = Label(fereastra, text="")
#countdown_label.pack(side="right", anchor="e")
countdown_label.grid(row=1, column=1)

livecounter_label = Label(fereastra, text="")
livecounter_label.grid(row=2, column=1)

# Codul pentru scor
label = Label(fereastra, text="Puncte: {}".format(puncte), font=('MsPain', 24), foreground="black") #fix this later bg="blue"
#label.pack(side="right", anchor="e")
label.grid(row=3, column=1)

# Asta pune in `Miscare` rankurile
countdown(countdown_label, 15)
livecounter(livecounter_label, 15)

 #I DID ITTTTTTTTTT WE HAVE CUSTOM BACKGROUNDDDDDDDDDD
canvas = Canvas(fereastra, height=AREA_HEIGHT, width=AREA_WIDTH)
#canvas.pack()
canvas.grid(row=1, column=0, rowspan=3)
bg_image = PhotoImage(file="assets/backgrounshiz.png")
canvas.create_image(0, 0, anchor=NW, image=bg_image)

#Le key bindings, gotta make it so you can bind them yourself
fereastra.bind('<Left>', lambda event: change_direction('left'))
fereastra.bind('<Right>', lambda event: change_direction('right'))
fereastra.bind('<Up>', lambda event: change_direction('up'))
fereastra.bind('<Down>', lambda event: change_direction('down'))

#Variabile
sarpe = Sarpe() #uhh da ok deci astea doua au legatura cu class Sarpe respectiv class Mancare
mancare = Mancare() #nu inteleg de ce nu ma lasa sa le pun pur si simplu jos separat
next_turn(sarpe, mancare)


fereastra.mainloop()
#Huge thanks to Codebro and W3schools