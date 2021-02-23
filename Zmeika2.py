import tkinter as tk
from random import randint

def Score(score):
    global text_score
    playing_field_cv.delete(text_score)
    text_score = playing_field_cv.create_text(60, 10, text=f'Зеленных шариков: {score}', fill='white')


class Stena:
    def __init__(self):
        self.sneta = [playing_field_cv.create_rectangle(0, 0, width, seg_size,
                                          fill='#000000'),
        playing_field_cv.create_rectangle(width-seg_size, seg_size, width, height,
                                          fill='#000000'),
        playing_field_cv.create_rectangle(width, height-seg_size, 0, height,
                                          fill='#000000'),
        playing_field_cv.create_rectangle(0, height-seg_size, seg_size, seg_size,
                                          fill='#000000')]


def main():
    global in_game
    if in_game:
        global pause_game
        if pause_game == 1:
            global s
            global foot
            global score
            s.move()
            head_segment = playing_field_cv.coords(s.segments[0].segment)
            x1, y1, x2, y2 = head_segment

            for i in range(2, len(s.segments)):
                if head_segment == playing_field_cv.coords(s.segments[i].segment):
                    in_game = False
            if playing_field_cv.coords(foot) == head_segment:
                create_foot(foot)
                s.add_segment()
                score += 1
                Score(score)

            for i in range(2, len(s.segments)):

                if (list(map(lambda x: x+2, head_segment[:2])) + list(map(lambda x: x-2, head_segment[2:]))) == playing_field_cv.coords(s.segments[i].segment):
                    in_game = False

            if (x1<seg_size or x2>width-seg_size) or (y1<seg_size or y2>height-seg_size):
                in_game = False

        else:
            pass

    else:
        pass
    root.after(100, main)


def create_foot(foot):
    posx = randint(1, (width-2*seg_size)/seg_size) * seg_size
    posy = randint(1, (height-2*seg_size)/seg_size) * seg_size
    playing_field_cv.coords(foot, posx, posy, posx+seg_size, posy+seg_size)


class Segment:
    def __init__(self, x, y, f='#000000'):
        self.segment = playing_field_cv.create_rectangle(x, y,
                                                         x + seg_size,
                                                         y + seg_size,
                                                         fill='green',
                                                         outline=f)


class Snake:
    def __init__(self, segmets):
        self.segments = segmets
        self.mapping = {'Down': (0, 1), 'Right': (1, 0), 'Left': (-1, 0), 'Up': (0, -1)}
        self.vector = self.mapping['Right']

    def move(self):
        x1, y1, x2, y2 = playing_field_cv.coords(self.segments[0].segment)
        playing_field_cv.coords(self.segments[0].segment,
                                x1+seg_size*self.vector[0], y1+seg_size*self.vector[1],
                                x2+seg_size*self.vector[0], y2+seg_size*self.vector[1])

        for index in range(1, len(self.segments)):
            x11, y11, x22, y22 = playing_field_cv.coords(self.segments[index].segment)
            playing_field_cv.coords(self.segments[index].segment, x1+2, y1+2, x2-2, y2-2)
            x1, y1, x2, y2 = x11-2, y11-2, x22+2, y22+2

    def change_direction(self, event):
        global in_game
        global pause_game
        if event.keysym == 'Escape':
            pause_game *= -1
        if (event.keysym in self.mapping) and self.mapping[event.keysym] != tuple(map(lambda a: a*-1,self.vector)):
            self.vector = self.mapping[event.keysym]

    def add_segment(self):
        self.segments += [Segment(*playing_field_cv.coords(self.segments[-1].segment)[0:2])]



root = tk.Tk()
root.title('Zmeika')
width = 800
height = 600
seg_size = 20
root.geometry(f'{width}x{height}+10+10')
root.resizable(width=False, height=False)
score = 0


in_game = True
pause_game = 1

playing_field_cv = tk.Canvas(width=width, height=height, bg='red')
playing_field_cv.focus_set()
playing_field_cv.grid()


stena1 = Stena()


s = Snake([Segment(60, seg_size,)])
[s.add_segment() for i in range(2)]


playing_field_cv.bind('<KeyPress>', s.change_direction)


foot = playing_field_cv.create_oval(0, 0, 20, 20, fill='green')
text_score = playing_field_cv.create_text(60, 10, text=f'Зеленных шариков: {score}', fill='white')

main()
create_foot(foot)

root.mainloop()
