from math import sqrt
from random import randrange as rnd, choice
from tkinter import *

root = Tk()
root.geometry('800x600')

canvas = Canvas(root, bg='white')
canvas.pack(fill=BOTH, expand=1)
colors = ['red', 'orange', 'yellow', 'green', 'blue']


def coords():
    global x, y, r, dx, dy
    dx = rnd(-5, 5)
    dy = rnd(-5, 5)
    x = rnd(100, 700)
    y = rnd(100, 500)
    r = rnd(30, 50)


def new_ball():
    global ball_id
    coords()
    canvas.delete('ball1')
    ball_id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=choice(colors), width=3, tag='ball1')
    root.after(rnd(1000, 1500), new_ball)


def move():
    global dx, dy, x, y
    x += dx
    y += dy
    if x + r >= 800 or x - r <= 0:
        dx = -dx
    if y + r >= 600 or y - r <= 0:
        dy = -dy
    canvas.move('ball1', dx, dy)
    root.after(30, move)


def count():
    global a1, a2, goals
    cathet1 = max(a1, x) - min(a1, x)
    cathet2 = max(a2, y) - min(a2, y)
    hypotenuse1 = sqrt(cathet1 ** 2 + cathet2 ** 2)
    if hypotenuse1 <= r:
        goals += 1
        root.after(100, canvas.delete('ball1'))


def coords2():
    global x2, y2, r2, dx2, dy2
    dx2 = rnd(-5, 5)
    dy2 = rnd(-5, 5)
    x2 = rnd(100, 700)
    y2 = rnd(100, 500)
    r2 = rnd(30, 50)


def new_ball2():
    global ball_id2
    coords2()
    canvas.delete('ball2')
    ball_id2 = canvas.create_oval(x2 - r2, y2 - r2, x2 + r2, y2 + r2, fill=choice(colors), width=3, tag='ball2')
    root.after(rnd(1000, 1500), new_ball2)


def move2():
    global dx2, dy2, x2, y2
    x2 += dx2
    y2 += dy2
    if x2 + r2 >= 800 or x2 - r2 <= 0:
        dx2 = -dx2
    if y2 + r2 >= 600 or y2 - r2 <= 0:
        dy2 = -dy2
    canvas.move('ball2', dx2, dy2)
    root.after(30, move2)


def count2():
    global a1, a2, goals
    cathet3 = max(a1, x2) - min(a1, x2)
    cathet4 = max(a2, y2) - min(a2, y2)
    hypotenuse2 = sqrt(cathet3 ** 2 + cathet4 ** 2)
    if hypotenuse2 <= r2:
        goals += 1
        root.after(100, canvas.delete('ball2'))


def click(event):
    global a1, a2
    a1 = event.x
    a2 = event.y
    count()
    count2()


def score():
    canvas.delete('text')
    canvas.create_text(100, 50, text=goals, font="Arials 25", tag='text')
    root.after(250, score)


def main():
    global goals
    goals = 0
    score()
    new_ball()
    move()
    new_ball2()
    move2()
    canvas.bind('<Button-1>', click)
    mainloop()


main()
