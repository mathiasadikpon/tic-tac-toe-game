import tkinter as tk
from tkinter import messagebox

class TicTacToeCanvas:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Resizable Canvas")

        self.player1_name = tk.StringVar(value="X")
        self.player2_name = tk.StringVar(value="O")
        self.board_size = tk.IntVar(value=3)
        self.board = []
        self.current_player = "X"
        self.canvas_cells = []

        self.create_widgets()
        self.configure_root_grid()

    def create_widgets(self):
        # Labels and entries
        tk.Label(self.root, text="Player X:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.player1_name).grid(row=0, column=1, sticky="ew")

        tk.Label(self.root, text="Player O:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.player2_name).grid(row=1, column=1, sticky="ew")

        tk.Label(self.root, text="Board Size:").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.board_size).grid(row=2, column=1, sticky="ew")

        # Start Button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)

        # Status label
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # Board frame
        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")

        # Restart button
        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 12),
                                        command=self.reset_game, state="disabled")
        self.restart_button.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=5)

    def configure_root_grid(self):
        # Make all root rows/columns expand
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.minsize(400, 400)

    def start_game(self):
        try:
            size = int(self.board_size.get())
            if size < 3 or size > 10:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Size", "Board size must be between 3 and 10.")
            return

        self.current_player = "X"
        self.board = [""] * (size * size)
        self.canvas_cells = []
        self.status_label.config(text=f"{self.player1_name.get()}'s turn (X)")
        self.restart_button.config(state="normal")

        # Clear previous board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Configure dynamic row/column weights
        for i in range(size):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

        for i in range(size * size):
            canvas = tk.Canvas(self.board_frame, bg="white", highlightthickness=1)
            canvas.grid(row=i // size, column=i % size, sticky="nsew")
            canvas.bind("<Configure>", lambda event, c=canvas: self.redraw_cell(c))
            canvas.bind("<Button-1>", lambda event, index=i: self.handle_click(index))
            canvas.symbol = None  # store what was drawn
            self.canvas_cells.append(canvas)

    def redraw_cell(self, canvas):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        canvas.create_oval(5, 5, w - 5, h - 5, fill="#f0f0f0", outline="black")
        if canvas.symbol == "X":
            canvas.create_line(10, 10, w - 10, h - 10, fill="red", width=3)
            canvas.create_line(w - 10, 10, 10, h - 10, fill="red", width=3)
        elif canvas.symbol == "O":
            canvas.create_oval(10, 10, w - 10, h - 10, outline="blue", width=3)

    def handle_click(self, index):
        if self.board[index] != "" or self.check_winner():
            return

        self.board[index] = self.current_player
        canvas = self.canvas_cells[index]
        canvas.symbol = self.current_player
        self.redraw_cell(canvas)

        if self.check_winner():
            winner = self.player1_name.get() if self.current_player == "X" else self.player2_name.get()
            messagebox.showinfo("Game Over", f"{winner} ({self.current_player}) wins!")
            self.status_label.config(text=f"{winner} wins!")
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
            lines.append([j * size + i for j in range(size)])             # columns

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
