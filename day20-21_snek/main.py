from turtle import Screen
from snek import Snek
from food import Food
from scoreboard import Scoreboard
import time


screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Sneaky Snek")
screen.tracer(0)

screen.listen()

scoreboard = Scoreboard()
sneaky_snek = Snek()
noms = Food()

# set direction key listeners
screen.onkey(key="w", fun=sneaky_snek.snek_north)
screen.onkey(key="a", fun=sneaky_snek.snek_west)
screen.onkey(key="s", fun=sneaky_snek.snek_south)
screen.onkey(key="d", fun=sneaky_snek.snek_east)

game_active = True
while game_active:
    screen.update()
    time.sleep(0.1)
    sneaky_snek.snek_move()
    if sneaky_snek.head.distance(noms) < 15:
        scoreboard.increase_score()
        noms.refresh_position()
        sneaky_snek.grow_snek()
    if sneaky_snek.has_collision():
        game_active = False
        scoreboard.game_over()

screen.exitonclick()
