import os
from tkinter import *
from random import choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
is_flipped = False  # To track if the card is currently flipped

def next_card():
    global current_card, is_flipped
    current_card = choice(to_learn)
    is_flipped = False  # Reset the flip state for the new card
    canvas.itemconfig(language, text="Mandarin", fill="black")
    canvas.itemconfig(card, image=card_back_q)
    canvas.itemconfig(word, text=current_card['Mandarin'], fill="black")

def flip_card(event=None): 
    global is_flipped
    if is_flipped:
        # Show the front side
        canvas.itemconfig(language, text="Mandarin", fill="black")
        canvas.itemconfig(word, text=current_card['Mandarin'], fill="black")
        canvas.itemconfig(card, image=card_back_q)
    else:
        # Show the back side
        canvas.itemconfig(language, text="Pinyin/English", fill="white")
        canvas.itemconfig(word, text=current_card['Pinyin/English'], fill="white")
        canvas.itemconfig(card, image=card_back_a)
    is_flipped = not is_flipped  # Toggle the flip state

def known():
    to_learn.remove(current_card)
    pandas.DataFrame(to_learn).to_csv("words_to_learn.csv", index=False)
    next_card()

def unknown():
    if not os.path.exists("words_to_learn.csv"):
        pandas.DataFrame(to_learn).to_csv("words_to_learn.csv", index=False)
    next_card()

def is_file_empty(file_path):
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0

# Try loading from words_to_learn.csv if it exists and is not empty
if os.path.exists("words_to_learn.csv") and not is_file_empty("words_to_learn.csv"):
    word_data = pandas.read_csv("words_to_learn.csv")
else:
    word_data = pandas.read_csv("mandarin_words.csv")

to_learn = word_data.to_dict(orient="records")

# Setup the window and UI elements
window = Tk()
window.title("Language Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

# Load images and create card before referencing
card_back_q = PhotoImage(file="images/card_front.png")
card_back_a = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_back_q)
language = canvas.create_text(400, 150, text="Mandarin", fill="black", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)
canvas.bind("<Button-1>", flip_card)  # Bind the click to flip_card function

# Buttons to indicate known/unknown words
wrong_img = PhotoImage(file="images/wrong.png")
Button(image=wrong_img, highlightthickness=0, borderwidth=0, command=unknown).grid(column=0, row=1)

right_img = PhotoImage(file="images/right.png")
Button(image=right_img, highlightthickness=0, borderwidth=0, command=known).grid(column=1, row=1)

next_card()
window.mainloop()