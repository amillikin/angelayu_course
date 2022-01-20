###This code will not work in repl.it as there is no access to the colorgram package here.###
##We talk about this in the video tutorials##
from turtle import Turtle, Screen
from random import choice
import colorgram

rgb_colors = []
colors = colorgram.extract('image.jpg', 30)
for color in colors:
    new_color = (color.rgb.r,
                 color.rgb.g,
                 color.rgb.b)
    rgb_colors.append(new_color)

t = Turtle()
t.speed(10)
t.penup()
t.setposition(-250.0,-250.0)
t.hideturtle()

screen = Screen()
screen.colormode(255)

for row in range(9):
    for col in range(9):
        t.dot(20,choice(rgb_colors))
        t.forward(50)
    if row % 2 == 0:
        t.left(90)
        t.forward(50)
        t.left(90)
    else:
        t.right(90)
        t.forward(50)
        t.right(90)

screen.exitonclick()

