import turtle
import random
import sqlite3
import turtlegame.level as level
from turtlegame.constants import *

connection = sqlite3.connect('turtle_events.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Events (
id INTEGER PRIMARY KEY AUTOINCREMENT,
type TEXT NOT NULL,
color TEXT,
direction TEXT
)
''')
cursor.execute('''
DELETE FROM Events  
               ''')
connection.commit()
# connection.close()

turtle.mode('logo')
turtle.colormode(255)
screen = turtle.Screen()
screen.setup(SCREEN_W, SCREEN_H)

cherepashka = turtle.Turtle()
cherepashka.speed(5)
cherepashka.shape("turtle")


def take_random_coordinate(screen, edge_lenght, cherepashka_position):
    random_coord = random.randint(-screen/2, screen/2 - edge_lenght)
    cherepashka_min = cherepashka_position - 80
    cherepashka_max = cherepashka_position + 80
    if random_coord < cherepashka_min or random_coord > cherepashka_max:
        return random_coord
    else:
        return take_random_coordinate(screen, edge_lenght, cherepashka_position)


class Square():
    def __init__(self, screen_w=SCREEN_W, screen_h=SCREEN_H, width=100, height=100, color=(50, 200, 50)):
        self.width = width
        self.height = height
        self.start_x = take_random_coordinate(
            screen_w, width, cherepashka.xcor())
        self.start_y = take_random_coordinate(
            screen_h, height, cherepashka.ycor())
        self.color = color


win_square = Square(SCREEN_W, SCREEN_H, random.randint(
    20, 100), random.randint(20, 100))

defeat_zones: list[Square] = []
for i in range(10):
    defeat_zones.append(Square(width=random.randint(
        20, 100), height=random.randint(20, 100), color=(200, 50, 50)))


def restricted_area_check(cherepashka):
    compensator = 20
    if cherepashka.xcor() > SCREEN_W/2 - compensator:
        cherepashka.goto(SCREEN_W/2 - compensator, cherepashka.ycor())
    if cherepashka.xcor() < -SCREEN_W/2 + compensator:
        cherepashka.goto(-SCREEN_W/2 + compensator, cherepashka.ycor())
    if cherepashka.ycor() > SCREEN_H/2 - compensator:
        cherepashka.goto(cherepashka.xcor(), SCREEN_H/2 - compensator)
    if cherepashka.ycor() < -SCREEN_H/2 + compensator:
        cherepashka.goto(cherepashka.xcor(), -SCREEN_H/2 + compensator)


cherepashka_step = 0


def make_move(angle, cherepashka):
    global cherepashka_step
    cherepashka_step = cherepashka_step + 1
    if cherepashka_step == 2:
        cherepashka_step = 0
        defeat_zones.append(Square(width=random.randint(
            20, 100), height=random.randint(20, 100), color=(50, 50, 200)))
        level.make_square(defeat_zones[-1], finish_turtle)
    if cherepashka.heading() == angle:
        cherepashka.fd(20)
        restricted_area_check(cherepashka)
        return
    if cherepashka.heading() == 0.0 and angle == 360:
        cherepashka.fd(20)
        restricted_area_check(cherepashka)
        return
    angle_compens = angle - cherepashka.heading()
    cherepashka.speed(0)
    cherepashka.rt(angle_compens)
    cherepashka.speed(5)
    cherepashka.fd(20)
    restricted_area_check(cherepashka)
    cursor.execute('''
    INSERT INTO Events (type) VALUES ('move')
    ''')
    connection.commit()


def win_check():
    x = cherepashka.xcor()
    y = cherepashka.ycor()
    if x >= win_square.start_x and x <= win_square.start_x + win_square.width and y >= win_square.start_y and y <= win_square.start_y + win_square.height:
        print('Вы победили!')
        exit(0)
    for defeat_square in defeat_zones:
        if x >= defeat_square.start_x and x <= defeat_square.start_x + defeat_square.width and y >= defeat_square.start_y and y <= defeat_square.start_y + defeat_square.height:
            print('Вы проиграли!')
            exit(0)


def walk_fd():
    global cherepashka
    make_move(360, cherepashka)
    enemy_moves()
    win_check()


def walk_bk():
    global cherepashka
    make_move(180, cherepashka)
    enemy_moves()
    win_check()


def walk_rt():
    global cherepashka
    make_move(90, cherepashka)
    enemy_moves()
    win_check()


def walk_lt():
    global cherepashka
    make_move(270, cherepashka)
    enemy_moves()
    win_check()


screen.onkeypress(walk_fd, 'w')
screen.onkeypress(walk_bk, 's')
screen.onkeypress(walk_rt, 'd')
screen.onkeypress(walk_lt, 'a')

finish_turtle = turtle.Turtle()
finish_turtle.speed(0)

level.make_square(win_square, finish_turtle)
for square in defeat_zones:
    level.make_square(square, finish_turtle)

enemy_counter = random.randint(2, 8)
enemy_turtles = [turtle.Turtle() for x in range(enemy_counter)]
enemy_turtles_on_position = []
compensator = 20
resp_positions = [
    {
        'x_min': -SCREEN_W/2 + compensator,
        'x_max': SCREEN_W/2 - compensator,
        'y_min': SCREEN_H/2 - compensator,
        'y_max': SCREEN_H/2 - compensator
    },
    {
        'x_min': SCREEN_W/2 - compensator,
        'x_max': SCREEN_W/2 - compensator,
        'y_min': -SCREEN_H/2 + compensator,
        'y_max': SCREEN_H/2 - compensator
    },
    {
        'x_min': -SCREEN_W/2 + compensator,
        'x_max': SCREEN_W/2 - compensator,
        'y_min': -SCREEN_H/2 + compensator,
        'y_max': -SCREEN_H/2 + compensator
    },
    {
        'x_min': -SCREEN_W/2 + compensator,
        'x_max': -SCREEN_W/2 + compensator,
        'y_min': -SCREEN_H/2 + compensator,
        'y_max': SCREEN_H/2 - compensator
    },
]
line_counter = 0
while len(enemy_turtles) > 0:
    if line_counter == len(resp_positions):
        line_counter = 0
    selected_line = resp_positions[line_counter]
    x = random.randint(selected_line['x_min'], selected_line['x_max'])
    y = random.randint(selected_line['y_min'], selected_line['y_max'])
    selected_turtle: turtle = enemy_turtles.pop()
    selected_turtle.shape("turtle")
    selected_turtle.speed(0)
    selected_turtle.color(250, 0, 0)
    selected_turtle.up()
    selected_turtle.goto(x, y)
    selected_turtle.down()
    enemy_turtles_on_position.append(selected_turtle)
    line_counter = line_counter + 1


def enemy_moves():
    for enemy_turtle in enemy_turtles_on_position:
        enemy_turtle.setheading(enemy_turtle.towards(cherepashka))
        enemy_turtle.fd(10)


screen.listen()
turtle.exitonclick()
