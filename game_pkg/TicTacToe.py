class TicTacToe:
    def __init__(self, size):
        self.size = size
        self.board = [""] * (size * size)
        self.current_player = "X"

    def make_move(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        size = self.size
        lines = []

        for i in range(size):
            lines.append([i * size + j for j in range(size)])  # rows
            lines.append([j * size + i for j in range(size)])  # columns

        lines.append([i * size + i for i in range(size)])  # diag TL-BR
        lines.append([i * size + (size - 1 - i) for i in range(size)])  # diag TR-BL

        for line in lines:
            if all(self.board[i] == self.current_player for i in line):
                return True
        return False

    def is_draw(self):
        return "" not in self.board

    def reset(self):
        self.board = [""] * (self.size * self.size)
        self.current_player = "X"
