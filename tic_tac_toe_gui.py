import tkinter as tk
from tkinter import messagebox

class TicTacToeCanvas:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Canvas Style")

        self.player1_name = tk.StringVar(value="X")
        self.player2_name = tk.StringVar(value="O")
        self.board_size = tk.IntVar(value=3)
        self.board = []
        self.current_player = "X"
        self.canvas_cells = []

        self.create_widgets()

    def create_widgets(self):
        # Player names and board size
        tk.Label(self.root, text="Player X:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.player1_name).grid(row=0, column=1)

        tk.Label(self.root, text="Player O:").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.player2_name).grid(row=1, column=1)

        tk.Label(self.root, text="Board Size:").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.board_size).grid(row=2, column=1)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=5)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.grid(row=4, column=0, columnspan=3)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=5, column=0, columnspan=3)

        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 12),
                                        command=self.reset_game, state="disabled")
        self.restart_button.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=5)

    def start_game(self):
        try:
            size = int(self.board_size.get())
            if size < 3 or size > 10:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Size", "Board size must be an integer between 3 and 10.")
            return

        self.current_player = "X"
        self.board = [""] * (size * size)
        self.canvas_cells = []
        self.status_label.config(text=f"{self.player1_name.get()}'s turn (X)")
        self.restart_button.config(state="normal")

        # Clear previous board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        for i in range(size * size):
            canvas = tk.Canvas(self.board_frame, width=60, height=60, bg="white", highlightthickness=1)
            canvas.grid(row=i // size, column=i % size)
            canvas.create_oval(5, 5, 55, 55, fill="#f0f0f0", outline="black")
            canvas.bind("<Button-1>", lambda event, index=i: self.handle_click(index))
            self.canvas_cells.append(canvas)

    def handle_click(self, index):
        if self.board[index] != "" or self.check_winner():
            return

        self.board[index] = self.current_player
        canvas = self.canvas_cells[index]
        symbol = self.current_player

        if symbol == "X":
            canvas.create_line(15, 15, 45, 45, fill="red", width=3)
            canvas.create_line(45, 15, 15, 45, fill="red", width=3)
        else:
            canvas.create_oval(15, 15, 45, 45, outline="blue", width=3)

        if self.check_winner():
            winner_name = self.player1_name.get() if self.current_player == "X" else self.player2_name.get()
            messagebox.showinfo("Game Over", f"{winner_name} ({self.current_player}) wins!")
            self.status_label.config(text=f"{winner_name} wins!")
            self.disable_board()
        elif "" not in self.board:
            messagebox.showinfo("Game Over", "It's a draw!")
            self.status_label.config(text="It's a draw!")
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            next_player = self.player1_name.get() if self.current_player == "X" else self.player2_name.get()
            self.status_label.config(text=f"{next_player}'s turn ({self.current_player})")

    def check_winner(self):
        size = self.board_size.get()
        lines = []

        for i in range(size):
            lines.append([i * size + j for j in range(size)])             # rows
            lines.append([j * size + i for j in range(size)])             # cols

        lines.append([i * size + i for i in range(size)])                 # diagonal TL-BR
        lines.append([i * size + (size - 1 - i) for i in range(size)])    # diagonal TR-BL

        for line in lines:
            if all(self.board[i] == self.current_player for i in line):
                return True
        return False

    def disable_board(self):
        for canvas in self.canvas_cells:
            canvas.unbind("<Button-1>")

    def reset_game(self):
        self.start_game()

# Run app
root = tk.Tk()
game = TicTacToeCanvas(root)
root.mainloop()
