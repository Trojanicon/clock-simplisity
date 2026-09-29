import tkinter
from datetime import datetime

BG = "black"
LIT = "#00ff66"
DIM = "#0a2e18"
REFRESH_MS = 50
USE_24H = True

W, H, T = 40, 90, 12
GAP = 12
DIGIT_COUNT = 6

SEGMENTS = {
    "0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
    "5": "afgcd", "6": "afgecd", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}

MODES = ["time", "date", "stopwatch"]
mode_index = 0

stopwatch_running = False
stopwatch_elapsed = 0.0
stopwatch_started_at = None

root = tkinter.Tk()
root.title("Digital Watch")
root.configure(bg=BG)

canvas = tkinter.Canvas(root, width=(W + GAP) * DIGIT_COUNT + 40, height=H + 60, bg=BG, highlightthickness=0)
canvas.pack(padx=10, pady=10)

digits = []
colon_dots = []
x = 20
for i in range(DIGIT_COUNT):
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
        top = canvas.create_oval(x + GAP / 2 - 4, y + H * 0.3, x + GAP / 2 + 4, y + H * 0.3 + 8, fill=DIM, outline="")
        bottom = canvas.create_oval(x + GAP / 2 - 4, y + H * 0.65, x + GAP / 2 + 4, y + H * 0.65 + 8, fill=DIM, outline="")
        colon_dots.append((top, bottom))
        x += GAP

status_label = tkinter.Label(root, text="", fg="#0a5c2e", bg=BG, font=("DejaVu Sans Mono", 14))
status_label.pack(pady=(0, 10))


def set_digit(bars, char):
    lit_segments = SEGMENTS.get(char, "")
    for name, item_id in bars.items():
        canvas.itemconfig(item_id, fill=LIT if name in lit_segments else DIM)


def set_colons(on):
    for top, bottom in colon_dots:
        color = LIT if on else DIM
        canvas.itemconfig(top, fill=color)
        canvas.itemconfig(bottom, fill=color)


def cycle_mode(event):
    global mode_index
    mode_index = (mode_index + 1) % len(MODES)


def toggle_format(event):
    global USE_24H
    USE_24H = not USE_24H


def stopwatch_toggle(event):
    global stopwatch_running, stopwatch_started_at
    if MODES[mode_index] != "stopwatch":
        return
    if stopwatch_running:
        stopwatch_running = False
    else:
        stopwatch_running = True
        stopwatch_started_at = datetime.now()


def stopwatch_reset(event):
    global stopwatch_running, stopwatch_elapsed, stopwatch_started_at
    if MODES[mode_index] != "stopwatch":
        return
    stopwatch_running = False
    stopwatch_elapsed = 0.0
    stopwatch_started_at = None


def stopwatch_total():
    total = stopwatch_elapsed
    if stopwatch_running and stopwatch_started_at:
        total += (datetime.now() - stopwatch_started_at).total_seconds()
    return total


def tick():
    global stopwatch_elapsed, stopwatch_started_at
    mode = MODES[mode_index]

    if mode == "time":
        now = datetime.now()
        text = now.strftime("%H%M%S") if USE_24H else now.strftime("%I%M%S")
        set_colons(now.microsecond < 500000)
        status_label.config(text=f"TIME   M: mode   F: 12/24h")

    elif mode == "date":
        now = datetime.now()
        day = now.strftime("%d")
        month = now.strftime("%m")
        year = now.strftime("%y")
        text = (day + month + year).ljust(DIGIT_COUNT)[:DIGIT_COUNT]
        set_colons(True)
        status_label.config(text=now.strftime("%A %d %B %Y") + "   M: mode")

    else:
        total = stopwatch_total()
        minutes = int(total // 60) % 100
        seconds = int(total % 60)
        hundredths = int((total - int(total)) * 100)
        text = f"{minutes:02d}{seconds:02d}{hundredths:02d}"
        set_colons(True)
        state = "RUNNING" if stopwatch_running else "STOPPED"
        status_label.config(text=f"STOPWATCH [{state}]   SPACE: start/stop   R: reset   M: mode")

    for bars, char in zip(digits, text):
        set_digit(bars, char if char.isdigit() else " ")

    root.after(REFRESH_MS, tick)


root.bind("<KeyPress-m>", cycle_mode)
root.bind("<KeyPress-M>", cycle_mode)
root.bind("<KeyPress-f>", toggle_format)
root.bind("<KeyPress-F>", toggle_format)
root.bind("<space>", stopwatch_toggle)
root.bind("<KeyPress-r>", stopwatch_reset)
root.bind("<KeyPress-R>", stopwatch_reset)
root.bind("<Escape>", lambda event: root.destroy())

tick()
root.mainloop()
 