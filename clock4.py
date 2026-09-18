import turtle
import time
import math

RADIUS = 200
REFRESH_MS = 50

wn = turtle.Screen()
wn.title("Analog Clock")
wn.bgcolor("black")
wn.setup(width=520, height=520)
wn.tracer(0)

face = turtle.Turtle()
face.hideturtle()
face.color("white")

hands = turtle.Turtle()
hands.hideturtle()


def polar(angle, r):
    rad = math.radians(90 - angle)
    return r * math.cos(rad), r * math.sin(rad)


def draw_ticks():
    for i in range(60):
        angle = i * 6
        major = i % 5 == 0
        inner = RADIUS - (20 if major else 10)
        face.penup()
        face.goto(polar(angle, inner))
        face.pensize(4 if major else 1)
        face.pendown()
        face.goto(polar(angle, RADIUS - 2))
    face.penup()


def draw_numbers():
    for hour in range(1, 13):
        x, y = polar(hour * 30, RADIUS - 42)
        face.goto(x, y - 9)
        face.write(str(hour), align="center", font=("Arial", 14, "bold"))


def draw_face():
    face.pensize(4)
    face.penup()
    face.goto(0, -RADIUS)
    face.setheading(0)
    face.pendown()
    face.circle(RADIUS)
    face.penup()
    draw_ticks()
    draw_numbers()


def draw_hand(angle, length, tail, color, width):
    hands.color(color)
    hands.width(width)
    hands.penup()
    hands.goto(polar(angle + 180, tail))
    hands.pendown()
    hands.goto(polar(angle, length))
    hands.penup()


def draw_labels(now):
    hands.color("gray")
    hands.goto(0, 60)
    hands.write(time.strftime("%H:%M:%S", now), align="center", font=("Arial", 14, "normal"))
    hands.goto(0, -85)
    hands.write(time.strftime("%a %d %b %Y", now), align="center", font=("Arial", 12, "normal"))


def update_clock():
    hands.clear()

    stamp = time.time()
    now = time.localtime(stamp)

    seconds = now.tm_sec + stamp % 1
    minutes = now.tm_min + seconds / 60
    hours = now.tm_hour % 12 + minutes / 60

    draw_labels(now)
    draw_hand(hours * 30, 90, 10, "deepskyblue", 6)
    draw_hand(minutes * 6, 130, 12, "limegreen", 4)
    draw_hand(seconds * 6, 160, 25, "red", 2)

    hands.goto(0, 0)
    hands.dot(12, "white")
    hands.dot(5, "red")

    wn.update()
    wn.ontimer(update_clock, REFRESH_MS)


draw_face()
update_clock()

try:
    wn.mainloop()
except turtle.Terminator:
    pass