from tkinter import *
from tkinter import messagebox
from quiz_brain import QuizBrain
from time import sleep

THEME_COLOR = "#375362"


class QuizInterface:


    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.is_right: bool
        self.window = Tk()
        self.window.title("Quizbert")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.label_score = Label(text="Score: 0", fg="white", bg=THEME_COLOR)
        self.label_score.grid(row=0, column=1)
        
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="question text",
            font=("Arial", 12, "italic"),
            fill=THEME_COLOR,
            )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)
        
        image_true = PhotoImage(file="./images/true.png")
        self.button_true = Button(image=image_true,
                                  highlightthickness=0,
                                  command=self.check_if_true)
        self.button_true.grid(row=2, column=0)

        image_false = PhotoImage(file="./images/false.png")
        self.button_false = Button(image=image_false,
                                   highlightthickness=0,
                                   command=self.check_if_false)
        self.button_false.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()


    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            question = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text,
                                   text=question)
        else:
            self.canvas.itemconfig(
                self.question_text,
                text="Your final score is: " +
                    f"{self.quiz.score}/{self.quiz.question_number}")
            self.button_true["state"] = "disabled"
            self.button_false["state"] = "disabled"



    def check_if_true(self):
        self.give_feedback(self.quiz.check_answer("true"))


    def check_if_false(self):
        self.give_feedback(self.quiz.check_answer("false"))


    def give_feedback(self, is_right: bool):
        if is_right:
            self.label_score.config(text=f"Score: {self.quiz.score}")
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        
        self.window.after(1000, self.get_next_question)


