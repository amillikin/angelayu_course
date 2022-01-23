import time
from turtle import Screen
from player import Player
from random import randint
from car_manager import CarManager
from scoreboard import Scoreboard


screen = Screen()

screen.setup(width=600, height=600)
screen.tracer(0)

screen.listen()

scoreboard = Scoreboard()
player = Player()
car_manager = CarManager()

screen.onkey(key="Up", fun=player.move_up)
screen.onkey(key="Down", fun=player.move_down)
screen.onkey(key="Left", fun=player.move_left)
screen.onkey(key="Right", fun=player.move_right)

game_is_on = True
while game_is_on:
    if randint(1,6) == 6:
        car_manager.spawn_car()

    car_manager.move_cars()
    time.sleep(0.1)
    screen.update()

    if player.reached_finish():
        scoreboard.update_level()
        player.reset_player()
        car_manager.increase_difficulty()
        
    
    if car_manager.collision_detected(player.pos()):
        scoreboard.game_over()
        game_is_on = False


screen.exitonclick()
