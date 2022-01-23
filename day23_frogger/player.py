from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.reset_player()


    def move_up(self):
        if self.ycor() <= 270:
            self.setheading(90)
            self.forward(MOVE_DISTANCE)


    def move_down(self):
        if self.ycor() >= -270:
            self.setheading(270)
            self.forward(MOVE_DISTANCE)


    def move_left(self):
        if self.xcor() >= -270:
            self.setheading(180)
            self.forward(MOVE_DISTANCE)


    def move_right(self):
        if self.xcor() <= 270:
            self.setheading(0)
            self.forward(MOVE_DISTANCE)


    def reached_finish(self):
        return self.ycor() >= FINISH_LINE_Y


    def reset_player(self):
        self.setheading(90)
        self.goto(STARTING_POSITION)
