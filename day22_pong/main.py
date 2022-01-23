from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time


screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("PyngPong")
screen.tracer(0)

screen.listen()

scoreboard = Scoreboard()

paddle_right = Paddle("right")
paddle_left = Paddle("left")
ball = Ball()

# set direction key listeners
screen.onkey(key="Up", fun=paddle_right.move_up)
screen.onkey(key="Down", fun=paddle_right.move_down)
screen.onkey(key="w", fun=paddle_left.move_up)
screen.onkey(key="s", fun=paddle_left.move_down)

game_active = True
while game_active:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # ball hits top or bottom
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # bounce if ball hits paddle
    if ((ball.distance(paddle_left) < 50 and ball.xcor() < -320) or 
        (ball.distance(paddle_right) < 50 and ball.xcor() > 320)):
        ball.bounce_x()

    # check for scoreboard_left
    if ball.xcor() > 380:
        scoreboard.increase_score("left")
        ball.reset_position()
    if ball.xcor() < -380:
        scoreboard.increase_score("right")
        ball.reset_position()

screen.exitonclick()
