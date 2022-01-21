from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Courier", 16, "normal")

class Scoreboard(Turtle):


    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.setpos(0, 270)
        self.color("white")
        self.current_score = 0
        self.refresh_score()    


    def increase_score(self):
        self.current_score += 1
        self.refresh_score()


    def refresh_score(self):
        self.clear()
        self.write(f"Score: {self.current_score}", align=ALIGNMENT, font=FONT)


    def game_over(self):
        self.home()
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
