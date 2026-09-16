import turtle
import time

wn = turtle.Screen()
wn.title("Analog Clock")
wn.bgcolor("black")
wn.tracer(0)

dial = turtle.Turtle()
dial.hideturtle()
dial.color("white")
dial.pensize(3)

clock = turtle.Turtle()
clock.hideturtle()

def draw_face():
    dial.penup()
    dial.goto(0, -200)
    dial.setheading(0)
    dial.pendown()
    dial.circle(200)

    for hour in range(1, 13):
        angle = 90 - (hour * 30)
        
        dial.penup()
        dial.goto(0, 0)
        dial.setheading(angle)
        dial.forward(180)
        dial.pendown()
        dial.pensize(4)
        dial.forward(20)
        dial.penup()
        dial.backward(45)
        pos = dial.pos()
        dial.goto(pos[0], pos[1] - 8)
        dial.write(str(hour), align="center", font=("Arial", 12, "bold"))

def draw_hand(angle, length, color, width):
    clock.color(color)
    clock.width(width)
    clock.penup()
    clock.goto(0, 0)
    clock.setheading(90 - angle)
    clock.pendown()
    clock.forward(length)

def update_clock():
    clock.clear()

    now = time.localtime()
    sec = now.tm_sec
    min = now.tm_min
    hour = now.tm_hour % 12

    sec_angle = sec * 6
    min_angle = min * 6 + sec * 0.1
    hour_angle = hour * 30 + min * 0.5

    draw_hand(sec_angle, 160, "red", 2)
    draw_hand(min_angle, 130, "green", 4)
    draw_hand(hour_angle, 90, "blue", 6)

    clock.penup()
    clock.goto(0, -5)
    clock.setheading(0)
    clock.color("white")
    clock.begin_fill()
    clock.circle(5)
    clock.end_fill()

    wn.update()

draw_face()

while True:
    update_clock()
    time.sleep(1)