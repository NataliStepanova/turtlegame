import turtle
import turtlegame.classes as classes


def make_square(square: classes.Square, trtl: turtle):
    trtl.speed(0)
    trtl.fillcolor(square.color)
    trtl.up()
    trtl.goto(square.start_x, square.start_y)
    trtl.down()
    trtl.begin_fill()
    trtl.fd(square.height)
    trtl.rt(90)
    trtl.fd(square.width)
    trtl.rt(90)
    trtl.fd(square.height)
    trtl.rt(90)
    trtl.fd(square.width)
    trtl.rt(90)
    trtl.end_fill()
