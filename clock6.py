import turtle
import time
import math
import tkinter
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

RADIUS = 190
GAP = 60
REFRESH_MS = 50
RING_SECONDS = 15
CLOCKS = [
    ("Local", None),
    ("New York", "America/New_York"),
    ("Tokyo", "Asia/Tokyo"),
]
THEMES = {
    "dark": {
        "bg": "black",
        "face": "white",
        "dim": "gray",
        "hour": "deepskyblue",
        "minute": "limegreen",
        "second": "red",
        "flash": "#4a0000",
    },
    "light": {
        "bg": "#f5f5f0",
        "face": "#222222",
        "dim": "#666666",
        "hour": "#1a4fd6",
        "minute": "#1a8a3a",
        "second": "#d62020",
        "flash": "#ffc8c8",
    },
    "neon": {
        "bg": "#0a0014",
        "face": "#00ffe1",
        "dim": "#b400ff",
        "hour": "#ff00aa",
        "minute": "#00ffe1",
        "second": "#ffee00",
        "flash": "#3a0060",
    },
}


class Clock:
    def __init__(self, cx, cy, radius, label, theme, tz_name=None):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.label = label
        self.theme = theme
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

    def set_theme(self, theme):
        self.theme = theme
        self.face.clear()
        self.draw_face()

    def polar(self, angle, r):
        rad = math.radians(90 - angle)
        return self.cx + r * math.cos(rad), self.cy + r * math.sin(rad)

    def draw_face(self):
        r = self.radius
        self.face.color(self.theme["face"])
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
        self.hands.color(self.theme["dim"])
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
        self.draw_hand(hours * 30, 0.47, 0.05, self.theme["hour"], 6)
        self.draw_hand(minutes * 6, 0.68, 0.06, self.theme["minute"], 4)
        self.draw_hand(seconds * 6, 0.84, 0.13, self.theme["second"], 2)

        self.hands.goto(self.cx, self.cy)
        self.hands.dot(12, self.theme["face"])
        self.hands.dot(5, self.theme["second"])


class Alarm:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.target = None
        self.fired = False
        self.ring_until = 0.0
        self.last_bell = 0.0
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()

    @property
    def ringing(self):
        return time.time() < self.ring_until

    @staticmethod
    def parse(text):
        try:
            hour, minute = text.strip().split(":")
            hour, minute = int(hour), int(minute)
        except ValueError:
            return None
        if 0 <= hour < 24 and 0 <= minute < 60:
            return hour, minute
        return None

    def prompt(self):
        text = self.screen.textinput("Set alarm", "Local time as HH:MM (leave blank to clear):")
        if text is None:
            return
        if not text.strip():
            self.clear()
            return
        parsed = self.parse(text)
        if parsed:
            self.target = parsed
            self.fired = False
            self.ring_until = 0.0

    def clear(self):
        self.target = None
        self.fired = False
        self.ring_until = 0.0

    def check(self):
        if self.target is None:
            return
        now = datetime.now()
        if (now.hour, now.minute) == self.target:
            if not self.fired:
                self.fired = True
                self.ring_until = time.time() + RING_SECONDS
        else:
            self.fired = False
        if self.ringing:
            self.ring()

    def ring(self):
        stamp = time.time()
        if stamp - self.last_bell < 1:
            return
        self.last_bell = stamp
        try:
            self.screen.getcanvas().bell()
        except tkinter.TclError:
            pass

    def refresh(self, theme, theme_name):
        self.pen.clear()
        if self.ringing:
            text = "ALARM!   Press C to dismiss"
            color = theme["second"]
        else:
            text = f"A: set alarm   C: clear   T: theme [{theme_name}]"
            if self.target:
                text = f"Alarm {self.target[0]:02d}:{self.target[1]:02d}   |   " + text
            color = theme["dim"]
        self.pen.color(color)
        self.pen.goto(self.x, self.y)
        self.pen.write(text, align="center", font=("Arial", 12, "normal"))


class App:
    def __init__(self):
        self.wn = turtle.Screen()
        self.wn.title("World Clocks")
        self.wn.setup(
            width=len(CLOCKS) * (2 * RADIUS + GAP) + GAP,
            height=2 * RADIUS + 180,
        )
        self.wn.tracer(0)

        self.theme_names = list(THEMES)
        self.theme_index = 0
        self.bg = None

        self.clocks = self.build_clocks()
        self.alarm = Alarm(self.wn, 0, -RADIUS - 60)
        self.bind_keys()

    @property
    def theme_name(self):
        return self.theme_names[self.theme_index]

    @property
    def theme(self):
        return THEMES[self.theme_name]

    def build_clocks(self):
        step = 2 * RADIUS + GAP
        start = -step * (len(CLOCKS) - 1) / 2
        return [
            Clock(start + i * step, 0, RADIUS, label, self.theme, tz)
            for i, (label, tz) in enumerate(CLOCKS)
        ]

    def bind_keys(self):
        actions = (
            ("t", self.cycle_theme),
            ("a", self.set_alarm),
            ("c", self.alarm.clear),
        )
        for key, action in actions:
            self.wn.onkeypress(action, key)
            self.wn.onkeypress(action, key.upper())
        self.wn.listen()

    def cycle_theme(self):
        self.theme_index = (self.theme_index + 1) % len(self.theme_names)
        for clock in self.clocks:
            clock.set_theme(self.theme)

    def set_alarm(self):
        self.alarm.prompt()
        self.wn.listen()

    def apply_background(self):
        flashing = self.alarm.ringing and int(time.time() * 3) % 2 == 0
        color = self.theme["flash"] if flashing else self.theme["bg"]
        if color != self.bg:
            self.wn.bgcolor(color)
            self.bg = color

    def tick(self):
        self.alarm.check()
        self.apply_background()
        for clock in self.clocks:
            clock.update()
        self.alarm.refresh(self.theme, self.theme_name)
        self.wn.update()
        self.wn.ontimer(self.tick, REFRESH_MS)

    def run(self):
        self.tick()
        try:
            self.wn.mainloop()
        except turtle.Terminator:
            pass


if __name__ == "__main__":
    App().run()