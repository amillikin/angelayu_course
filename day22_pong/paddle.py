from turtle import Turtle
PADDLE_POSITION = {"left": (-350, 0),
                  "right": (350, 0)}
PADDLE_HEIGHT = 1
PADDLE_WIDTH = 5

class Paddle(Turtle):


    def __init__(self, paddle_side):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.shapesize(stretch_wid=PADDLE_WIDTH, stretch_len=PADDLE_HEIGHT)
        self.penup()
        self.goto(PADDLE_POSITION[paddle_side])


    def move_up(self):
        if self.ycor() < 230:
            self.goto(self.xcor(), self.ycor() + 20)


    def move_down(self):
        if self.ycor() > -230:
            self.goto(self.xcor(), self.ycor() - 20)

