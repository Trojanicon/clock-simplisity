# clock-simplisity

clock.py:
A minimal analog clock implementation using a basic while True loop and time.sleep(1). It redraws the entire clock face and hands each second with animation tracing disabled (tracer(0)) to eliminate flicker.

clock2.py:
An event-driven analog clock that replaces the blocking while loop with Turtle's native ontimer scheduling. It redraws the face and hands on a fixed 500x500 window without disabling screen tracing.

clock3.py:
The most complete design, separating static and dynamic elements using two turtles. It draws a detailed face once—including tick marks and hour numbers (1–12) and updates only the moving clock hands each second.

clock4.py:
A polished event-driven analog clock. It draws the full face once—tick marks and hour numbers—and updates only the hands every 50 ms via ontimer, giving a smooth sweeping second hand, hand tails, a center dot, and a digital time and date display.

clock5.py:
Refactors the clock into a Clock class with every dimension scaled from a single radius, and adds support for multiple timezones side by side in one window, driven by a shared ontimer loop.

clock6.py:
A multi-timezone analog clock built from a Clock class, an Alarm class and an App class. Each clock draws its face once (tick marks and hour numbers) and redraws only the hands, digital time and date every 50 ms via ontimer, giving a smooth sweeping second hand. Several clocks can share one window, each set to an IANA timezone (Local, New York, Tokyo by default). Keyboard controls: T cycles between dark, light and neon themes, A sets a local-time alarm, and C clears or dismisses it. When the alarm fires, the background flashes and the Tk bell rings for 15 seconds.

clock7.py:
Builds on clock6 by adding a custom alarm sound. Looks for a sound file next to the script and plays it per-platform (winsound on Windows, afplay on macOS, paplay on Linux), falling back to the system bell if the file is missing. Adds a P key to preview the alarm sound on demand, and shows the active sound source in the status line.

clock_advanced1.py:
Merges clock7 with a "mash to load" splash screen shown before the clock window opens. A custom image fills a progress bar that only rises while a key is held or pressed repeatedly, decaying back down when idle, with rotating loading-flavor status text. Still a work in progress.

digital1.py:
The start of a separate digital-watch series. Uses plain tkinter instead of Turtle, since a digital display is just text rather than drawn hands, keeping it much simpler and lighter than the analog series. Shows time and date in an LCD-style green-on-black display, with an F key to toggle 12/24-hour format.

digital2.py:
Rebuilds the LCD display with plain rectangle segments instead of a system font, using a SEGMENTS maps and no classes just a flat list of segment IDs per digit and a couple of small functions. Much shorter than the first attempt, at the cost of a blockier look than a true seven-segment shape. Blinking colon and F-key 12/24h toggle carried over from digital1.

digital3.py:
Adds mode switching on top of digital2's segment rendering. M cycles between Time, Date and Stopwatch, reusing the same six digits for all three. The colon now blinks correctly once per second. Stopwatch mode tracks elapsed time from a start timestamp rather than counting ticks, so it stays accurate under lag—Space starts/stops it, R resets it.

digital4.py:
Adds backlight simulation to digital3. After 5 seconds of no input(this is an issue coz when the stopwatch is running, ina go blxk pia, will think on hoe to fix that later), the display dims to a muted green and the status line reads "asleep—press any key to wake." Any keypress or click instantly restores full brightness. All existing controls; M, F, Space, R.... still work and count as activity.

improvements by the day