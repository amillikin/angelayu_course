from turtle import Screen, Turtle
from random import randint

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Sneaky Snek")


def snek_north():
    if not sneks[0].heading() == 90:
        sneks[0].setheading(90)


def snek_west():
    if not sneks[0].heading() == 180:
        sneks[0].setheading(180)


def snek_south():
    if not sneks[0].heading() == 270:
        sneks[0].setheading(270)


def snek_east():
    if not sneks[0].heading() == 0:
        sneks[0].setheading(0)


def snek_move(sneks_list):
    # set each segment's position to match the segment ahead of it
    for snek in range(len(sneks_list)-1, 0, -1):
        sneks_list[snek].setposition(sneks_list[snek-1].position()) 
    sneks_list[0].forward(20)


def spawn_food():
    pass


def check_food():
    pass

def check_collision():
    head_pos = sneks[0].pos()
    if head_pos[0] in (-300, 300) or head_pos[1] in (-300, 300):
        return True
    else:
        for snek in range(1, len(sneks)):
            if head_pos == sneks[snek].pos():
                return True
        return False

# setup sneks
sneks = [Turtle(), Turtle(), Turtle()]
for i in range(3):
    sneks[i].shape("square")
    sneks[i].color("white")
    sneks[i].penup()
    sneks[i].goto((-1 * 20 * i + 40) , 0)

sneaky_dot_snek = Turtle()
sneaky_dot_snek.hideturtle()

screen.listen()

# set direction key listeners
screen.onkey(key="w", fun=snek_north) # north
screen.onkey(key="a", fun=snek_west) # west
screen.onkey(key="s", fun=snek_south) # south
screen.onkey(key="d", fun=snek_east) # east

snek_collision = False

while not snek_collision:
    snek_move(sneks)
    snek_collision = check_collision()
    check_food()

screen.exitonclick()
