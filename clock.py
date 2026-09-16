import turtle
import time

wn = turtle.Screen()
wn.title("Analog Clock")
wn.bgcolor("black")
wn.tracer(0)

clock = turtle.Turtle()
clock.hideturtle()
clock.pensize(3)

def draw_hand(angle, length, color, width):
    clock.color(color)
    clock.width(width)
    clock.penup()
    clock.goto(0, 0)
    clock.setheading(90 - angle)
    clock.pendown()
    clock.forward(length)

def draw_clock():
    clock.clear()

    clock.penup()
    clock.goto(0, -200)
    clock.setheading(0) 
    clock.pendown()
    clock.color("white")
    clock.pensize(3)
    clock.circle(200)

    now = time.localtime()
    sec = now.tm_sec
    min = now.tm_min
    hour = now.tm_hour % 12

    sec_angle = sec * 6
    min_angle = min * 6 + sec * 0.1
    hour_angle = hour * 30 + min * 0.5

    # Draw hands
    draw_hand(sec_angle, 150, "red", 1)
    draw_hand(min_angle, 120, "green", 3)
    draw_hand(hour_angle, 80, "blue", 5)

    wn.update()

while True:
    draw_clock()
    time.sleep(1)