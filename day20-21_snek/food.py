from turtle import Turtle
import random


class Food(Turtle):


    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.color("white")
        self.speed("fastest")
        self.refresh_position()


    def refresh_position(self):
        x_pos = random.randint(-270, 270)
        y_pos = random.randint(-270, 270)
        self.goto(x_pos, y_pos)
