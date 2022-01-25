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
        self.high_score = 0
        self.get_high_score()
        self.update_scoreboard()

    def increase_score(self):
        self.current_score += 1
        self.update_scoreboard()


    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.current_score} "
                   f"High Score: {self.high_score}",
                   align=ALIGNMENT, font=FONT)


    def reset(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score
        self.current_score = 0
        self.update_scoreboard()


    def update(self):
        self.home()
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)


    def get_high_score(self):
        try:
            with open(file="high_score.txt", mode="r", encoding="UTF-8") as reader:
                self.high_score = int(reader.readline())
        except FileNotFoundError:
            pass

    def record_high_score(self):
        try:
            with open(file="high_score.txt", mode="w", encoding="UTF-8") as writer:
                writer.write(str(self.high_score))
        except FileNotFoundError:
            pass
