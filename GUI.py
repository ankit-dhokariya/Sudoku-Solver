import pygame as pg
import time
import os
from game import *
from puzzle_generator import *
pg.font.init()

width = 630
height = 630
background_color = (30, 30, 30)
pad = 80

class Grid:

    board = puzzle(3)

    def __init__(self, rows, cols, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height + pad
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.model = None
        self.update_model()
        self.screen = screen

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if check_validity(self.model, val, (row, col)) and solution(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

        return True

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, screen):

        space = self.width / self.cols
        for i in range(self.rows + 1):
            if i % (self.rows // 3) == 0:
                thickness = 5
            else:
                thickness = 1
            pg.draw.line(screen, (115, 204, 255), (0, i * space + pad), (self.width, i * space + pad), thickness)
            pg.draw.line(screen, (115, 204, 255), (i * space, pad), (i * space, self.height), thickness)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(screen)

    def select(self, row, col):

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):

        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):

        if pos[0] < self.width and pad < pos[1] < self.height:
            space = self.width / 9
            x = pos[0] // space
            y = (pos[1] - pad) // space
            return (int(y), int(x))
        else:
            return None

    def over(self):

        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False

        return True

    def gui_solution(self, animation):

        find = find_blank(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if check_validity(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                if animation is True:
                    self.cubes[row][col].draw_change(self.screen, True)
                self.update_model()
                pg.display.update()
                if animation is True:
                    pg.time.delay(25)

                if self.gui_solution(animation):
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                if animation is True:
                    self.cubes[row][col].draw_change(self.screen, False)
                pg.display.update()
                if animation is True:
                    pg.time.delay(25)

        return False


class Cube:

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False

    def draw(self, screen):

        font = pg.font.SysFont("comicsans", 40)

        space = self.width / 9
        x = self.col * space
        y = self.row * space + pad

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            screen.blit(text, (x + 5, y + 5))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, (255, 255, 255))
            screen.blit(text, (x + (space / 2 - text.get_width() / 2), y + (space / 2 - text.get_height() / 2)))

        if self.selected:
            pg.draw.rect(screen, (255, 0, 0), (x, y, space, space), 3)

    def draw_change(self, screen, g=True):
        font = pg.font.SysFont("comicsans", 40)

        space = self.width / 9
        x = self.col * space
        y = (self.row * space) + pad

        pg.draw.rect(screen, background_color, (x, y, space, space), 0)

        text = font.render(str(self.value), 1, (255, 255, 255))
        screen.blit(text, (x + (space / 2 - text.get_width() / 2), y + (space / 2 - text.get_height() / 2)))
        if g:
            pg.draw.rect(screen, (0, 255, 0), (x, y, space, space), 3)
        else:
            pg.draw.rect(screen, (255, 0, 0), (x, y, space, space), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def redraw_window(screen, board, time, strikes, end, background_color, button_color, animation, gaveup):

    screen.fill(background_color)
    font = pg.font.SysFont("comicsans", 40)

    ani_text = font.render("Animation", 1, (255, 255, 255))
    screen.blit(ani_text, (10, 30))

    on = pg.image.load("Images\\on.png")
    off = pg.image.load("Images\\off.png")
    if animation is True:
        screen.blit(on, (ani_text.get_width() + 20, 23))
    else:
        screen.blit(off, (ani_text.get_width() + 20, 23))

    text = font.render("Time: " + format_time(time), 1, (255, 255, 255))
    screen.blit(text, (width - 180, height + 35 + pad))
    pg.draw.line(screen, (255, 255, 255), (width - 180, height + 60 + pad), (width - 20, height + 60 + pad))

    if end is True:
        if gaveup is True:
            gaveup_t = font.render("Try harder", 1, (255, 255, 0))
            screen.blit(gaveup_t, (width / 2 - 70, height + 35 + pad))
        elif gaveup is False:
            yes = pg.image.load("Images\\yes.png")
            screen.blit(yes, (width / 2 - 30, height + 20 + pad))
        text = font.render("Game Over", 1, (255, 0, 0))
        screen.blit(text, (35, height + 35 + pad))
    elif end is False:
        if gaveup is False:
            if strikes < 3:
                giveup = font.render("Solve", 1, (0, 0, 0))
                pg.draw.rect(screen, button_color, (width / 2 - 40, height + 30 + pad, 83, 38), 0)
                screen.blit(giveup, (width / 2 - 35, height + 35 + pad))
                heart = pg.image.load("Images\\heart.png")
                for i in range(3 - strikes):
                    screen.blit(heart, (35 * i + 10, height + 35 + pad))
            elif strikes >= 3:
                no = pg.image.load("Images\\no.png")
                screen.blit(no, (width / 2 - 30, height + 20 + pad))
                text = font.render("Game Over", 1, (255, 0, 0))
                screen.blit(text, (35, height + 35 + pad))

    board.draw(screen)

def format_time(secs):

    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " {0:02}:{1:02}".format(minute, sec)
    return mat

def main():

    start = time.time()
    strikes = 0
    key = None
    end = False
    animation = True
    x = -1
    y = -1
    skip = False
    gaveup = False
    complete = False
    a = 30
    b = 40

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (a, b)
    pg.init()
    screen = pg.display.set_mode((width, height + 100 + pad))
    pg.display.set_caption("Sudoku")
    screen.fill(background_color)
    board = Grid(9, 9, 630, 630, screen)
    button_color = (200, 200, 0)

    running = True

    while running:

        if end is False:
            elap_time = round(time.time() - start)

        pos = pg.mouse.get_pos()
        if skip is False:
            if width / 2 - 40 < pos[0] < width / 2 + 43 and height + 30 + pad < pos[1] < height + 68 + pad:
                button_color = (255, 255, 120)
            else:
                button_color = (200, 200, 0)
        else:
            skip = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9
                if event.key == pg.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pg.K_DOWN and y < 8:
                    if y < 0:
                        x = 0
                        y = 0
                    else:
                        y += 1
                    board.select(y, x)

                if event.key == pg.K_UP and y > 0:
                    y -= 1
                    board.select(y, x)

                if event.key == pg.K_RIGHT and x < 8:
                    if x < 0:
                        x = 0
                        y = 0
                    else:
                        x += 1
                    board.select(y, x)

                if event.key == pg.K_LEFT and x > 0:
                    x -= 1
                    board.select(y, x)

                if event.key == pg.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            None
                        else:
                            strikes += 1
                        key = None

                        if board.over():
                            complete = True
                            end = True
                        elif strikes >= 3:
                            end = True

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()

                if width / 2 - 40 < pos[0] < width + 43 and height + 30 + pad < pos[1] < height + 68 + pad:
                    button_color = (200, 200, 0)
                    redraw_window(screen, board, elap_time, strikes, complete, background_color, button_color, animation, gaveup)
                    board.gui_solution(animation)
                    gaveup = True
                    skip = True
                    if board.over():
                        complete = True
                        end = True

                if 143 < pos[0] < 205 and 23 < pos[1] < 63:
                    animation = not(animation)

                clicked = board.click(pos)
                if clicked:
                    y, x = clicked
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.sketch(key)

        redraw_window(screen, board, elap_time, strikes, complete, background_color, button_color, animation, gaveup)
        pg.display.update()


main()
pg.quit()
