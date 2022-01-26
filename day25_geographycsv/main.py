import turtle
import pandas

IMAGE = "./blank_states_img.gif"
FONT = ("Courier", 12, "normal")

screen = turtle.Screen()
screen.title("U.S. States Game")
screen.addshape(IMAGE)
turtle.shape(IMAGE)

state_data = pandas.read_csv("./50_states.csv")
state_list = state_data.state.to_list()

writer = turtle.Turtle()
writer.penup()
writer.hideturtle()

game_active = True
correct_count = 0
states_guessed = []
prompt_msg = "Try to guess a state!"
title_msg = f"Guess a State! ({correct_count}/50)"
while game_active:
    answer_state = screen.textinput(title=title_msg, prompt=prompt_msg)
    if answer_state == None:
        game_active = False
        states_left = list(set(state_list) - set(states_guessed))
        states_left_dict = {"state": states_left}
        df = pandas.DataFrame(states_left_dict)
        df.to_csv("states_left.csv")
    else:
        answer_state = answer_state.title()
        if answer_state in state_list:
            state_row = state_data[state_data["state"] == answer_state]
            writer.goto(int(state_row.x), int(state_row.y))
            writer.write(answer_state.title(), align="center", font=FONT)
            states_guessed.append(answer_state)
            correct_count += 1
            title_msg = f"Guess a State! ({correct_count}/50)"
            prompt_msg = "Correct! Guess again!"
            game_active = correct_count != 50
        else:
            prompt_msg = "Sorry, that's incorrect. Try again."

screen.exitonclick()
