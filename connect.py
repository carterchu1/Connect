import random


class Connect:
    def __init__(self, row, col):
        self.row = row
        self.board = [[Node() for i in range(row)] for j in range(col)]

    def neighbor(self):
        edges = [(0, 1), (1, 0), (-1, 0), (0, -1),
                 (0, 1), (1, 0), (-1, 0), (0, -1)]
        count = 0
        k = random.randint(0, self.row ** 2)
        while count < self.row ** 2:
            k = k % (self.row ** 2)
            i = k // self.row
            j = k % self.row
            if self.board[i][j].path == 0:
                kk = random.randint(0, 4)
                for a in range(kk, kk+4):
                    dx, dy = edges[a]
                    i2 = i + dx
                    j2 = j + dy
                    if i2 >= 0 and j2 >= 0 and i2 < self.row and j2 < self.row:
                        if self.board[i2][j2].path == 0:
                            return (k, i2, j2)
            count += 1
            k += 1
        return (-1, -1, -1)

    def check_neighbor(self, r1, c1, r2, c2):
        count = 0
        edges = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in edges:
            r = r1 + dx
            c = c1 + dy
            if 0 <= r and r < self.row and 0 <= c and c < self.row:
                if self.board[r][c].find_set() == self.board[r2][c2].find_set():
                    count += 1
        return count <= 1

    def valid_next(self, row, col):
        edges = [(0, 1), (1, 0), (-1, 0), (0, -1), (0, 1), (1, 0), (-1, 0), (0, -1)]
        kk = random.randint(0, 3)
        for a in range(kk, kk+4):
            dx, dy = edges[a]
            row2 = row + dx
            col2 = col + dy
            if row2 >= 0 and col2 >= 0 and row2 < self.row and col2 < self.row:
                if self.board[row2][col2].path == 0 and self.check_neighbor(row2, col2, row, col):
                    return (row2, col2)
        return (-1, -1)

    def add_path(self, pathnum):
        k, r2, c2 = self.neighbor()
        if k == -1:
            return False
        r1 = k // self.row
        c1 = k % self.row
        self.board[r1][c1].endpoint = True
        self.board[r1][c1].path = pathnum
        self.board[r2][c2].path = pathnum
        self.board[r1][c1].find_set().set_union(self.board[r2][c2].find_set())
        while True:
            r1 = r2
            c1 = c2
            r2, c2 = self.valid_next(r2, c2)
            if r2 == -1:
                self.board[r1][c1].endpoint = True
                break
            self.board[r2][c2].path = pathnum
            self.board[r1][c1].find_set().set_union(self.board[r2][c2].find_set())
        return True

    def print_board(self):
        print("Board:")
        for col in self.board:
            for node in col:
                if node.endpoint:
                    print("|{:2d} |".format(node.path), end='')
                elif node.path == 0:
                    print("| X |", end='')
                else:
                    print("|   |", end='')
            print("")
        print("\nSolution:")
        for col in self.board:
            for node in col:
                if node.path != 0:
                    print("|{:2d} |".format(node.path), end='')
                else:
                    print("| X |", end='')
            print("")

    def generate(self):
        count = 1
        while True:
            if not self.add_path(count):
                break
            else:
                count += 1


class Node:
    def __init__(self):
        self.parent = None
        self.rank = 0
        self.path = 0
        self.endpoint = False

    def find_set(self):
        if self.parent is not None:
            return self.parent
        return self

    def set_union(self, node):
        this = self.find_set()
        other = node.find_set()
        if (this.rank > other.rank):
            other.parent = this
        else:
            this.parent = other
            if (this.rank == other.rank):
                other.rank += 1
