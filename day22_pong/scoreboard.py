from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Courier", 40, "normal")
SCORE_POSITION = {"left": (-100, 200),
                  "right": (100, 200)}

class Scoreboard(Turtle):


    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("white")
        self.current_score_l = 0
        self.current_score_r = 0
        self.refresh_score()


    def increase_score(self, side):
        if side == "left":
            self.current_score_l += 1
        if side == "right":
            self.current_score_r += 1
        self.refresh_score()


    def refresh_score(self):
        self.clear()
        self.setpos(SCORE_POSITION["left"])
        self.write(f"{self.current_score_l}", align=ALIGNMENT, font=FONT)
        self.setpos(SCORE_POSITION["right"])
        self.write(f"{self.current_score_r}", align=ALIGNMENT, font=FONT)


    def game_over(self):
        self.home()
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
