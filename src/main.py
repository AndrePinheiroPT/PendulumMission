from sense_hat import SenseHat
from time import time
from math_tools import *
from math import *

file = open('data.txt', 'w')
file.write('Data points:')

viewer = Viewer()
plot = Graph(viewer, **{'unit_y': 100, 'unit_x':50})
sense = SenseHat()
sense.clear()

start = time()
can_plot = False
dots = []

def led_state(color):
    for i in range(3, 5):
        for j in range(3, 5):
            sense.set_pixel(i, j, color)
led_state((0, 255, 0))


def check_joystick(event):
    global can_plot, start
    if event.action == 'pressed':
        start = time()
        can_plot = True
        led_state((255, 0, 0))

def main():
    global start, can_plot, file
    
    end = time()
    t = round(end - start, 2)
    raw = sense.get_accelerometer_raw()
    pitch_x = round(acos((raw['x'] if raw['x'] >= -1 else -1) if raw['x'] <= 1 else 1) - pi/2, 3)
    print(f'Pitch x: {pitch_x}  Time: {t}')

    sense.stick.direction_any = check_joystick
    if can_plot:
        plot.cartesian_plane()
        dots.append([t, pitch_x])
        for d in dots:
            plot.dot(d)

        file = open('data.txt', 'a')
        file.write(f'\n[{t}, {pitch_x}]')

viewer.set_slides([main])
viewer.init()

    
    