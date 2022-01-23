from turtle import Turtle
FONT = ("Courier", 20, "normal")
TEXT_POSITION = (-210, 250)

class Scoreboard(Turtle):
    

    def __init__(self):
        super().__init__()
        self.level = 0
        self.hideturtle()
        self.penup()
        self.goto(TEXT_POSITION)
        self.update_level()

    
    def update_level(self):
        self.level += 1
        self.clear()
        self.write(f"Level: {self.level}", align="center", font=FONT)


    def game_over(self):
        self.home()
        self.write("GAME OVER", align="center", font=FONT)
