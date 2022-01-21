from turtle import Turtle, Screen
from random import randint

turtle_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
turtle_start = [(-230, 125),
                (-230, 75),
                (-230, 25),
                (-230, -25),
                (-230, -75),
                (-230, -125)]
s = Screen()
s.setup(width=500, height=400)
s.bgcolor("black")

user_choice = s.textinput(title="Make your bet!",
                          prompt="Which turtle will win the race? Pick a color: ").lower()

t = []
for i in range(6):
    turtle = Turtle(shape="turtle")
    turtle.hideturtle()
    turtle.color(turtle_colors[i])
    turtle.penup()
    turtle.goto(turtle_start[i])
    turtle.showturtle()
    t.append(turtle)

race_over = False

winners = []

while not race_over:
    for turtle in t:
        turtle.forward(5*randint(1,5))
        if turtle.xcor() >= 250:
            race_over = True
            winners.append(turtle.pencolor())

if user_choice in winners:
    print("You bet correctly\n"
          f"Winners: {winners}")
else:
    print("I'm sorry, your bet did not win.\n"
          f"Winners: {winners}")

s.exitonclick()
