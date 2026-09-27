import tkinter
from datetime import datetime

BG = "black"
LIT = "#f2f7f4"
DIM = "#000000"
REFRESH_MS = 200
USE_24H = True

W, H, T = 40, 90, 12
GAP = 12

SEGMENTS = {
    "0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
    "5": "afgcd", "6": "afgecd", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}

root = tkinter.Tk()
root.title("Digital Watch")
root.configure(bg=BG)

canvas = tkinter.Canvas(root, width=(W + GAP) * 6 + 40, height=H + 60, bg=BG, highlightthickness=0)
canvas.pack(padx=10, pady=10)

digits = []
x = 20
for i in range(6):
    y = 20
    bars = {
        "a": canvas.create_rectangle(x, y, x + W, y + T, fill=DIM, outline=""),
        "g": canvas.create_rectangle(x, y + H / 2 - T / 2, x + W, y + H / 2 + T / 2, fill=DIM, outline=""),
        "d": canvas.create_rectangle(x, y + H - T, x + W, y + H, fill=DIM, outline=""),
        "f": canvas.create_rectangle(x, y, x + T, y + H / 2, fill=DIM, outline=""),
        "e": canvas.create_rectangle(x, y + H / 2, x + T, y + H, fill=DIM, outline=""),
        "b": canvas.create_rectangle(x + W - T, y, x + W, y + H / 2, fill=DIM, outline=""),
        "c": canvas.create_rectangle(x + W - T, y + H / 2, x + W, y + H, fill=DIM, outline=""),
    }
    digits.append(bars)
    x += W + GAP
    if i in (1, 3):
        canvas.create_oval(x + GAP / 2 - 4, y + H * 0.3, x + GAP / 2 + 4, y + H * 0.3 + 8, fill=LIT, outline="")
        canvas.create_oval(x + GAP / 2 - 4, y + H * 0.65, x + GAP / 2 + 4, y + H * 0.65 + 8, fill=LIT, outline="")
        x += GAP

date_label = tkinter.Label(root, text="", fg="#0a5c2e", bg=BG, font=("DejaVu Sans Mono", 14))
date_label.pack(pady=(0, 10))


def set_digit(bars, char):
    lit_segments = SEGMENTS.get(char, "")
    for name, item_id in bars.items():
        canvas.itemconfig(item_id, fill=LIT if name in lit_segments else DIM)


def toggle_format(event):
    global USE_24H
    USE_24H = not USE_24H


def tick():
    now = datetime.now()
    text = now.strftime("%H%M%S") if USE_24H else now.strftime("%I%M%S")
    for bars, char in zip(digits, text):
        set_digit(bars, char)
    date_label.config(text=now.strftime("%a %d %b %Y"))
    root.after(REFRESH_MS, tick)


root.bind("<KeyPress-f>", toggle_format)
root.bind("<KeyPress-F>", toggle_format)
root.bind("<Escape>", lambda event: root.destroy())

tick()
root.mainloop()