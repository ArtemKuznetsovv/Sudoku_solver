import pygame
from sudoku_solver import *
from pygame.locals import *
import boards
import time

# grid-size
WINDOWMULTIPLIER = 6
WINDOWSIZE = 90
WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER + 60
WHITE = (255, 255, 255)
LIGHTGREY = (200, 200, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 204, 0)
RED = (255 , 0, 0)
GAMEWINDOWHEIGHT = WINDOWWIDTH


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        # Call this method to draw the button on the screen
        pygame.draw.rect(
            win,
            self.color,
            (self.x,
             self.y,
             self.width,
             self.height),
            0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text,
                     (self.x + (self.width / 2 - text.get_width() / 2),
                      self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Cell:
    def __init__(self, num, row, col, width, height):
        self.num = num
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.temp = 0  # temp value before validation
        self.selected = False

    def draw_cell(self, surface):
        font = pygame.font.Font("font.ttf", 20)

        posx = self.col * self.width
        posy = self.row * self.height

        if self.temp != 0 and self.num == 0:
            text = font.render(str(self.temp), True, (180, 180, 180))
            surface.blit(text, (posx + self.width / 2, posy + 5))
        elif self.num != 0:
            text = font.render(str(self.num), True, (0, 0, 0))
            surface.blit(text,
                         (posx + int(self.width / 2),
                          posy + int(self.width / 2)))

        if self.selected:
            pygame.draw.rect(surface, (60, 120, 220),
                             (posx, posy, self.width, self.height), 3)

        return None

    # def update_window(self,surface) #Update bonus elemnets such time . etc


class Board:
    # board here is the numbers representing it at the start
    def __init__(self, rows, cols, board, height, width):
        self.rows = rows
        self.cols = cols
        self.board = board  # for logical board
        self.height = height
        self.width = width
        self.cells = [ [ Cell(board[i][j], i , j , width / 9 , height / 9) for j in range(self.cols)] for i in range(self.rows)]  # for user board
        self.select_cell = None

    def update_board(self, value, cord):
        self.board[cord.row][cord.col] = value

    def place_number(self, value):  # places a number in selected cell
        cube = Cube(self.select_cell.row, self.select_cell.col)
        if self.cells[cube.row][cube.col].num == 0:
            self.cells[cube.row][cube.col].num = value
            self.update_board(value, cube)
            solver = Solver(self.board)
            if solver.is_valid(value, cube) and solver.solve():
                return True
            self.cells[cube.row][cube.col].num = 0
            self.cells[cube.row][cube.col].temp = 0
            self.update_board(0, cube)
            return False

    # gets the pos of cell clicked on and selects it

    def select(self, cord):
        self.select_cell = cord
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[cord.row][cord.col].selected = True

    def is_valid_click(self, cord):  # returns if the cube user clicked on , is valid
        if cord[0] < self.width and cord[1] < self.height:
            cell_size = self.width / 9
            row_num = int(cord[1] // cell_size)
            col_num = int(cord[0] // cell_size)
            return Cube(row_num, col_num)
        return None

    def draw_temp(self, val):  # temporary selection , before we find out it is a valid number
        row = self.select_cell.row
        col = self.select_cell.col
        self.cells[row][col].temp = val

    def draw_grid(self, surface, button,time):
        surface.fill(WHITE)
        cell_size = int(self.width / 9)
        # verticles
        count = 0
        for x in range(0, self.height, cell_size):
            if count % 3 == 0 and count != 0:
                pygame.draw.line(surface, BLACK, (x, 0), (x, self.height))
            else:
                pygame.draw.line(surface, LIGHTGREY, (x, 0), (x, self.height))
            count += 1

            # horizontal
        count = 0
        for y in range(0, self.width + 60, cell_size):
            if count % 3 == 0 and count != 0:
                pygame.draw.line(surface, BLACK, (0, y), (self.width, y))
            else:
                pygame.draw.line(surface, LIGHTGREY, (0, y), (self.width, y))
            count += 1

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw_cell(surface)

        fnt = pygame.font.SysFont("comicsans", 40)
        text = fnt.render("Time: " + self.format_time(time), 1, (0, 0, 0))
        surface.blit(text, (360, 560))
        font = pygame.font.Font("font.ttf", 20)
        button.draw(surface)

        return None

    def clear(self):
        row = self.select_cell.row
        col = self.select_cell.col
        if self.cells[row][col].num == 0:
            self.cells[row][col].temp = 0

    def check_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].num == 0:
                    return False

        return True

    def format_time(self,secs):
        sec = secs % 60
        minute = secs // 60
        hour = minute // 60

        mat = " " + str(minute) + ":" + str(sec)
        return mat


def main():

    pygame.init()
    surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Sudoku game')

    board = Board(9, 9, boards.board_normal, GAMEWINDOWHEIGHT, WINDOWWIDTH)#Change Board Here
    solver_game = Solver(board.board)


    running = True
    error_button=False
    solve_button = Button(YELLOW, 60, 540, 100, 50, "Solve") # x , y, width , height
    start = time.time()
    while running:
        running_time=round(time.time()-start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit button
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None

                if event.key == pygame.K_RETURN:
                    if board.select_cell is not None:
                        cord = board.select_cell
                        value = board.cells[cord.row][cord.col].temp
                        if value != 0:
                            if board.place_number(
                                    value):  # might want to add icon on bottom
                                print("Success")
                                key = None
                            else:
                                print("Wrong")  # System for wrong strikes
                            if board.check_finished():
                                print("Done")
                                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # player selected
                temp_cord = pygame.mouse.get_pos() # pygame coordinates
                if solve_button.isOver(temp_cord): # clicked to solve ?

                    if solver_game.check_mistakes() and solver_game.solve() :


                        for i in range(board.rows):
                            for j in range(board.cols):
                                board.cells[i][j].num = board.board[i][j]

                        board.draw_grid(surface, solve_button, running_time)
                    else:
                        cnt_solv = Button(RED,WINDOWHEIGHT/3,WINDOWWIDTH/3, 300, 200, "Cant Solve This")
                        board.draw_grid(surface, cnt_solv , running_time)
                        error_button = True

                cord = board.is_valid_click(temp_cord) # did the user clicked in bounds of the window
                if cord:
                    board.select(cord) # select this cell
                    key = None

        if board.select_cell and key is not None: # Selected cell and the user typed in a number
            board.draw_temp(key)
        if not error_button:
            board.draw_grid(surface, solve_button,running_time)

        pygame.display.update()


if __name__ == '__main__':
    main()
