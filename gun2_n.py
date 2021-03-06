from random import randrange as rnd, choice
import tkinter as tk
import math
import time


root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=1)


class Ball:
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.ay = 0.9
        self.color = choice(['blue', 'green', 'grey'])
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        # self.live = 30

    def set_coords(self):
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy += self.ay
        if self.x + self.r >= 800 - self.vx or self.x + self.r <= 0 - self.vx:
            self.vx = -self.vx * 0.7
        if self.y + self.r >= 540 - self.vy or self.y <= 0 - self.vy:
            self.vy = -self.vy * 0.7
            self.ay *= 0.9
        if self.ay < 0.2:
            self.vx *= 0.9
            self.vy = 0
        if self.ay < 0.19 and self.vx < 0.2:
            canvas.delete(self.id)
        self.x += self.vx
        self.y += self.vy
        canvas.move(self.id, self.vx, self.vy)

    def hit_test(self, obj):
        cathet_x = max(self.x, obj.x) - min(self.x, obj.x)
        cathet_y = max(self.y, obj.y) - min(self.y, obj.y)
        space = math.sqrt(cathet_x ** 2 + cathet_y ** 2)
        if space <= self.r + obj.r:
            return True
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте t1.
        Args:
            t1: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

    def ball_delete(self):
        canvas.delete(self.id)


class Texts:
    def __init__(self):
        global balls
        self.points = 0
        self.screen1 = canvas.create_text(400, 50, text='', font='28')
        self.hits_screen = canvas.create_text(30, 30, text=self.points, font='28')

    def hits(self):
        canvas.itemconfig(self.hits_screen, text=self.points)

    def try_s(self, obj):
        canvas.itemconfig(self.screen1, text='Вы уничтожили цель за ' + str(len(obj)) + ' выстрелов')

        # ??? canvas.itemconfig( screen1, text='' )

    def delete_hits(self):
        canvas.itemconfig(self.screen1, text='')
        canvas.itemconfig(self.hits_screen, text='')


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canvas.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event=''):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball()
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, event=''):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, 20, 450,
                      20 + max(self.f2_power, 20) * math.cos(self.an),
                      450 + max(self.f2_power, 20) * math.sin(self.an)
                      )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1

    def gun_delete(self):
        canvas.delete(self.id)


class Target:
    def __init__(self):
        self.x = rnd(600, 750)
        self.y = rnd(50, 450)
        self.r = rnd(2, 50)
        self.vx = rnd(1, 10)
        self.vy = rnd(1, 10)
        self.color = 'red'
        self.points = 0
        self.live = 1
        self.id = canvas.create_oval(0, 0, 0, 0)

    def new_target(self):
        """ Инициализация новой цели. """

        canvas.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
        canvas.itemconfig(self.id, fill=self.color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.delete(self.id)  # canvas.coords( self.id, -10, -10, -10, -10 )
        self.points += points

    def move_t(self):
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= 800 - self.vx or self.x + self.r <= 600 - self.vx:
            self.vx = -self.vx
        if self.y + self.r >= 540 - self.vy or self.y <= 0 - self.vy:
            self.vy = -self.vy
        canvas.move(self.id, self.vx, self.vy)


balls = []


def new_game():
    global balls
    t1 = Target()
    t2 = Target()
    g1 = Gun()
    z = 0.03
    t1.live = 1
    t2.live = 1
    balls = []
    text = Texts()
    t1.new_target()
    t2.new_target()
    canvas.bind('<Button-1>', g1.fire2_start)
    canvas.bind('<ButtonRelease-1>', g1.fire2_end)
    canvas.bind('<Motion>', g1.targeting)
    while t1.live or t2.live:
        for b in balls:
            b.move()
            if b.hit_test(t1) and t1.live:
                t1.live = 0
                t1.hit()
                text.try_s(balls)
            if b.hit_test(t2) and t2.live:
                t2.live = 0
                t2.hit()
                text.try_s(balls)
        text.points = t1.points + t2.points
        text.hits()
        t1.move_t()
        t2.move_t()
        canvas.update()
        time.sleep(z)
        g1.targeting()
        g1.power_up()
    text.delete_hits()
    g1.gun_delete()

    root.after(200, new_game)


new_game()

root.mainloop()
