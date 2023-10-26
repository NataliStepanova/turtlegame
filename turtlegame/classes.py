from turtlegame.constants import *
from turtlegame.utils import take_random_coordinate


class Square():
    def __init__(self, cherepashka, screen_w=SCREEN_W, screen_h=SCREEN_H, width=100, height=100, color=(50, 200, 50)):
        self.width = width
        self.height = height
        self.start_x = take_random_coordinate(
            screen_w, width, cherepashka.xcor())
        self.start_y = take_random_coordinate(
            screen_h, height, cherepashka.ycor())
        self.color = color
