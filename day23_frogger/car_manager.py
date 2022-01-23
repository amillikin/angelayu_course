from turtle import Turtle
from random import choice

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
POSSIBLE_START_Y = [-250, -230, -210, -190, -170, -150, -130, -110, -90,
                  -70, -50, -30, -10, 10, 30, 50, 70, 90, 110, 130, 150, 170,
                  190, 210, 230, 250]
STARTING_MOVE_DISTANCE = 5 
MOVE_INCREMENT = 10


class CarManager():
    

    def __init__(self):
        self.cars = []
        self.reusable_cars = []
        self.move_distance = STARTING_MOVE_DISTANCE
        

    def spawn_car(self):
        # let's check if we can reuse an old car to prevent memory leaks
        for car in self.cars:
            if car.xcor() <= -300:
                self.reusable_cars.append(car)
                self.cars.remove(car)

        if len(self.reusable_cars) > 0:
            new_car = self.reusable_cars[-1]
            self.reusable_cars.pop()
        else:
            new_car = Turtle()
            new_car.shape("square")
            new_car.penup()
            new_car.setheading(180)
            new_car.shapesize(stretch_len=2)

        new_car.color(choice(COLORS))
        new_car.setpos(300, choice(POSSIBLE_START_Y))
        self.cars.append(new_car)


    def move_cars(self):
        for car in self.cars:
            car.forward(self.move_distance)


    def increase_difficulty(self):
        self.move_distance += MOVE_INCREMENT


    def collision_detected(self, player_position):
        for car in self.cars:
            if car.distance(player_position) < 20:
                return True

        return False
