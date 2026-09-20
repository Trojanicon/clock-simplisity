import turtle
import time
import math
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

RADIUS = 190
GAP = 60
REFRESH_MS = 50
CLOCKS = [
    ("Home", None),
    ("New York", "America/New_York"),
    ("Tokyo", "Asia/Tokyo"),
    ("London", "Europe/London")
]


class Clock:
    def __init__(self, cx, cy, radius, label, tz_name=None):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.label = label
        self.tz = self.load_tz(tz_name)
        self.face = self.make_turtle()
        self.hands = self.make_turtle()
        self.draw_face()

    @staticmethod
    def load_tz(tz_name):
        if tz_name is None:
            return None
        try:
            return ZoneInfo(tz_name)
        except ZoneInfoNotFoundError:
            raise SystemExit(f"No timezone data for {tz_name}. Try: pip install tzdata")

    @staticmethod
    def make_turtle():
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        return t

    def polar(self, angle, r):
        rad = math.radians(90 - angle)
        return self.cx + r * math.cos(rad), self.cy + r * math.sin(rad)

    def draw_face(self):
        r = self.radius
        self.face.color("white")
        self.face.pensize(4)
        self.face.goto(self.cx, self.cy - r)
        self.face.setheading(0)
        self.face.pendown()
        self.face.circle(r)
        self.face.penup()

        for i in range(60):
            angle = i * 6
            major = i % 5 == 0
            inner = r * (0.9 if major else 0.95)
            self.face.goto(self.polar(angle, inner))
            self.face.pensize(4 if major else 1)
            self.face.pendown()
            self.face.goto(self.polar(angle, r * 0.99))
            self.face.penup()

        size = max(8, int(r * 0.075))
        for hour in range(1, 13):
            x, y = self.polar(hour * 30, r * 0.79)
            self.face.goto(x, y - size * 0.65)
            self.face.write(str(hour), align="center", font=("Arial", size, "bold"))

        self.face.goto(self.cx, self.cy + r + 14)
        self.face.write(self.label, align="center", font=("Arial", 16, "bold"))

    def draw_hand(self, angle, length, tail, color, width):
        self.hands.color(color)
        self.hands.width(width)
        self.hands.penup()
        self.hands.goto(self.polar(angle + 180, self.radius * tail))
        self.hands.pendown()
        self.hands.goto(self.polar(angle, self.radius * length))
        self.hands.penup()

    def draw_labels(self, now):
        digital = max(8, int(self.radius * 0.07))
        date = max(8, int(self.radius * 0.06))
        self.hands.color("gray")
        self.hands.goto(self.cx, self.cy + self.radius * 0.3)
        self.hands.write(now.strftime("%H:%M:%S"), align="center", font=("Arial", digital, "normal"))
        self.hands.goto(self.cx, self.cy - self.radius * 0.45)
        self.hands.write(now.strftime("%a %d %b %Y"), align="center", font=("Arial", date, "normal"))

    def update(self):
        self.hands.clear()

        now = datetime.now(self.tz)
        seconds = now.second + now.microsecond / 1_000_000
        minutes = now.minute + seconds / 60
        hours = now.hour % 12 + minutes / 60

        self.draw_labels(now)
        self.draw_hand(hours * 30, 0.47, 0.05, "deepskyblue", 6)
        self.draw_hand(minutes * 6, 0.68, 0.06, "limegreen", 4)
        self.draw_hand(seconds * 6, 0.84, 0.13, "red", 2)

        self.hands.goto(self.cx, self.cy)
        self.hands.dot(12, "white")
        self.hands.dot(5, "red")


def build_clocks(specs):
    step = 2 * RADIUS + GAP
    start = -step * (len(specs) - 1) / 2
    return [
        Clock(start + i * step, 0, RADIUS, label, tz)
        for i, (label, tz) in enumerate(specs)
    ]


def main():
    wn = turtle.Screen()
    wn.title("World Clocks")
    wn.bgcolor("black")
    wn.setup(width=len(CLOCKS) * (2 * RADIUS + GAP) + GAP, height=2 * RADIUS + 140)
    wn.tracer(0)

    clocks = build_clocks(CLOCKS)

    def tick():
        for clock in clocks:
            clock.update()
        wn.update()
        wn.ontimer(tick, REFRESH_MS)

    tick()

    try:
        wn.mainloop()
    except turtle.Terminator:
        pass


if __name__ == "__main__":
    main()