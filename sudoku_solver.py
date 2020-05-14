
class Cube:
    def __init__(self, row, col):
        self.row = row
        self.col = col


class Solver:
    def __init__(self, board):
        self.board = board

    def check_mistakes(self):
        count= [[0 for i in range(len(self.board[0])+1)]for j in range(len(self.board))]

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                count[i][self.board[i][j]] += 1

        for i in range(len(count)):
            for j in range(len(count[0])):
                if count[i][j] > 1 and j != 0:
                    return False

        return True




    def solve(self):
        start = self.find_spot()

        if start is None:
            return True  # solved
        row = start.row
        col = start.col
        for i in range(1, 10):
            if self.is_valid(i, start):
                self.board[row][col] = i
                if self.solve():
                    return True
                else:
                    self.board[row][col] = 0
        return False

    def print_board(self):
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print('- ' * 10)
            for j in range(len(self.board[i])):
                if j % 3 == 0 and j != 0:
                    print('|', end="")
                print(self.board[i][j], end=" ")
            print("\n")

    def find_spot(self):
        len_row = len(self.board)
        for i in range(len_row):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    found = Cube(i, j)
                    return found
        return None

    def is_valid(self, num, cord):
        row = cord.row
        col = cord.col
        #check in row
        for i in range(len(self.board[row])):
            if self.board[row][i] == num and i != col:
                return False
        # check col
        for i in range(len(self.board)):
            if num == self.board[i][col] and i != row:
                return False

        # check 3x3 cube
        cube_row = int((row // 3) * 3)
        cube_col = int((col // 3) * 3)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[cube_row][cube_col] == num and (
                        j != col and i != row):
                    return False
                cube_col += 1
            cube_col -= 3
            cube_row += 1

        return True



