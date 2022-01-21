from turtle import Turtle
STARTING_POSITIONS = [(0,0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20

class Snek:


    def __init__(self):
        self.snek_segments = []
        self.create_snek()
        self.head = self.snek_segments[0]


    def create_snek(self):
        # setup self.snek_segments
        self.snek_segments = [Turtle(), Turtle(), Turtle()]
        for i in range(3):
            self.snek_segments[i].shape("square")
            self.snek_segments[i].color("white")
            self.snek_segments[i].penup()
            self.snek_segments[i].goto(STARTING_POSITIONS[i])
    

    def grow_snek(self):
        new_segement = Turtle()
        new_segement.hideturtle()
        new_segement.shape("square")
        new_segement.color("white")
        new_segement.penup()
        tail_segment_pos = self.snek_segments[len(self.snek_segments)-1].pos()
        new_segement.goto(tail_segment_pos)
        new_segement.showturtle()

        self.snek_segments.append(new_segement)


    def snek_north(self):
        if not self.snek_segments[0].heading() == 270:
            self.snek_segments[0].setheading(90)
    
    
    def snek_west(self):
        if not self.snek_segments[0].heading() == 0:
            self.snek_segments[0].setheading(180)
    
    
    def snek_south(self):
        if not self.snek_segments[0].heading() == 90:
            self.snek_segments[0].setheading(270)
    
    
    def snek_east(self):
        if not self.snek_segments[0].heading() == 180:
            self.snek_segments[0].setheading(0)
    

    def snek_move(self):
        # set each segment's position to match the segment ahead of it
        for snek in range(len(self.snek_segments)-1, 0, -1):
            self.snek_segments[snek].setposition(self.snek_segments[snek-1].position()) 
        self.head.forward(MOVE_DISTANCE)


    def has_collision(self):
        if (self.head.xcor() < -280 or 
                self.head.xcor() > 280 or 
                self.head.ycor() < -280 or 
                self.head.ycor() > 280):
            return True
        else:
            for snek in self.snek_segments[1:]:
                if self.head.distance(snek) < 10:
                    return True
            return False
