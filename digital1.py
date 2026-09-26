import tkinter
from datetime import datetime

BG = "black"
FG = "#00ff66"
DIM = "#0a3d1f"
FONT_TIME = ("DejaVu Sans Mono", 64, "bold")
FONT_DATE = ("DejaVu Sans Mono", 16)
REFRESH_MS = 200
USE_24H = True


def format_time(now):
    if USE_24H:
        return now.strftime("%H:%M:%S")
    return now.strftime("%I:%M:%S %p")


def format_date(now):
    return now.strftime("%a %d %b %Y")


class DigitalWatch:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Digital Watch")
        self.root.configure(bg=BG)

        self.time_label = tkinter.Label(
            self.root, text="", font=FONT_TIME, fg=FG, bg=BG
        )
        self.time_label.pack(padx=40, pady=(30, 0))

        self.date_label = tkinter.Label(
            self.root, text="", font=FONT_DATE, fg=DIM, bg=BG
        )
        self.date_label.pack(pady=(0, 30))

        self.root.bind("<KeyPress-f>", self.toggle_format)
        self.root.bind("<KeyPress-F>", self.toggle_format)
        self.root.bind("<Escape>", lambda event: self.root.destroy())

    def toggle_format(self, event):
        global USE_24H
        USE_24H = not USE_24H

    def tick(self):
        now = datetime.now()
        self.time_label.config(text=format_time(now))
        self.date_label.config(text=format_date(now))
        self.root.after(REFRESH_MS, self.tick)

    def run(self):
        self.tick()
        self.root.mainloop()


if __name__ == "__main__":
    DigitalWatch().run()