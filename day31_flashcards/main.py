from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    flash_card_data = pandas.read_csv("./data/cards_to_learn.csv")
except FileNotFoundError:
    flash_card_data = pandas.read_csv("./data/french_words.csv")
finally:
    flash_card_dict = flash_card_data.to_dict(orient="records")
    
current_card = {}

def get_next_card():
    global current_card, card_timer
    window.after_cancel(card_timer)
    canvas.itemconfig(card_image, image=card_front_img)
    current_card = random.choice(flash_card_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"])
    card_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"])
    canvas.itemconfig(card_image, image=card_back_img)


def known_card():
    flash_card_dict.remove(current_card)
    cards_to_learn_data = pandas.DataFrame(flash_card_dict)
    cards_to_learn_data.to_csv("./data/cards_to_learn.csv", index=False)
    get_next_card()


window = Tk()
window.title("éclat")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 32, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 48, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, 
                        highlightthickness=0,
                        command=get_next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="./images/right.png")
known_button = Button(image=check_image, 
                      highlightthickness=0, 
                      command=known_card)
known_button.grid(row=1, column=1)

get_next_card()

window.mainloop()
