from tkinter import*
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
TIMER = 5000
COUNT = 1

# -------------------- CREATE FLSH CARD ------------------------- #

data = []
learnt = []

# get data list, if you run code for the first time get data from original file, if not get data from words to learn csv
try:
    data_frame = pandas.read_csv(f"data/danish{COUNT}_words_to_learn.csv")
except FileNotFoundError:
    original_data_frame = pandas.read_csv(f"data/danish{COUNT}.csv")
    data = original_data_frame.to_dict(orient="records")
else:
    data = data_frame.to_dict(orient="records")

# get data from known words csv, so you can add new known words to list
# if you run code for the first time, list of already known words is empty
try:
    data_frame_known = pandas.read_csv(f"data/danish{COUNT}_words_learnt.csv")
except FileNotFoundError:
    learnt = []
else:
    learnt = data_frame_known.to_dict(orient="records")


english = ""
danish = ""


def generate_card():
    global english, danish, flip_timer
    window.after_cancel(flip_timer)

    random_index = random.randint(0, len(data))
    danish = data[random_index]["Danish"]

    english = data[random_index]["English"]
    canvas.itemconfig(flash_text, text=danish, fill="black")
    canvas.itemconfig(card_title, text="Danish", fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(TIMER, func=flip_card)

# ----------------------- FLIP CARD ----------------------------- #


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(flash_text, text=english, fill="white")
    canvas.itemconfig(card_background, image=card_back)

# --------------------- REMOVE CARD ----------------------------- #


def remove_flash_card():
    data.remove({"Danish": danish, "English": english})
    generate_card()
    new_data = pandas.DataFrame(data)
    new_data.to_csv(f"data/danish{COUNT}_words_to_learn.csv", index=False)
    new_word = {
        "Danish": danish,
        "English": english
    }
    learnt.append(new_word)
    new_learnt_data = pandas.DataFrame(learnt)
    new_learnt_data.to_csv(f"data/danish{COUNT}_words_learnt.csv", index=False)


# ---------------------- UI Interface --------------------------- #

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front)

card_title = canvas.create_text(400, 150, text="Danish", font=("Arial", 40, "italic"))
flash_text = canvas.create_text(400, 263, text="elsker", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


image_left_button = PhotoImage(file="images/wrong.png")
image_right_button = PhotoImage(file="images/right.png")

button_left = Button(image=image_left_button, highlightthickness=0, command=generate_card)
button_left.grid(column=0, row=1)

button_right = Button(image=image_right_button, highlightthickness=0, command=remove_flash_card)
button_right.grid(column=1, row=1)

generate_card()

window.mainloop()
