# clock-simplisity
clock.py: 
A minimal analog clock implementation using a basic while True loop and time.sleep(1). It redraws the entire clock face and hands each second with animation tracing disabled (tracer(0)) to eliminate flicker.

clock2.py: 
An event-driven analog clock that replaces the blocking while loop with Turtle's native ontimer scheduling. It redraws the face and hands on a fixed 500x500 window without disabling screen tracing.

clock3.py: 
The most complete design, separating static and dynamic elements using two turtles. It draws a detailed face once—including tick marks and hour numbers (1–12) and updates only the moving clock hands each second.