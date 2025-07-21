import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.player1_name = tk.StringVar(value="X")
        self.player2_name = tk.StringVar(value="O")
        self.board_size = tk.IntVar(value=2)
        self.buttons = []
        self.board = []
        self.current_player = "X"

        self.create_widgets()

    def create_widgets(self):
        # Player Name Inputs
        tk.Label(self.root, text="Player X:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.player1_name).grid(row=0, column=1)

        tk.Label(self.root, text="Player O:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.player2_name).grid(row=1, column=1)

        # Board Size Input
        tk.Label(self.root, text="Board Size (e.g. 2 for 2x2):").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.board_size).grid(row=2, column=1)

        # Start Button (full width)
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=5)

        # Turn status label
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.grid(row=4, column=0, columnspan=3)

        # Board Frame
        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=5, column=0, columnspan=3)

        # Restart Button
        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 12),
                                        command=self.reset_game, state="disabled")
        self.restart_button.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=5)

    def start_game(self):
        name1 = self.player1_name.get().strip()
        name2 = self.player2_name.get().strip()
        size = self.board_size.get()

        if not name1 or not name2:
            messagebox.showwarning("Missing Name", "Please enter both player names.")
            return
        if size < 2 or size > 10:
            messagebox.showwarning("Invalid Size", "Please enter a size between 2 and 10.")
            return

        self.current_player = "X"
        self.board = [""] * (size * size)
        self.status_label.config(text=f"{name1}'s turn (X)")
        self.clear_board()

        self.buttons = []
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        for i in range(size * size):
            btn = tk.Button(self.board_frame, text="", font=("Arial", 20),
                            width=4, height=2, command=lambda i=i: self.handle_click(i))
            btn.grid(row=i // size, column=i % size)
            self.buttons.append(btn)

        self.restart_button.config(state="normal")

    def handle_click(self, index):
        if self.board[index] == "" and not self.check_winner():
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner():
                winner = self.player1_name.get() if self.current_player == "X" else self.player2_name.get()
                messagebox.showinfo("Game Over", f"{winner} ({self.current_player}) wins!")
                self.status_label.config(text=f"{winner} wins!")
                self.disable_buttons()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a draw!")
                self.status_label.config(text="It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                next_name = self.player1_name.get() if self.current_player == "X" else self.player2_name.get()
                self.status_label.config(text=f"{next_name}'s turn ({self.current_player})")

    def check_winner(self):
        size = self.board_size.get()
        lines = []

        # Rows and columns
        for i in range(size):
            lines.append([i * size + j for j in range(size)])             # row
            lines.append([j * size + i for j in range(size)])             # column

        # Diagonals
        lines.append([i * size + i for i in range(size)])                 # top-left to bottom-right
        lines.append([i * size + (size - 1 - i) for i in range(size)])    # top-right to bottom-left

        for line in lines:
            if all(self.board[i] == self.current_player for i in line):
                return True
        return False

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def clear_board(self):
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()

    def reset_game(self):
        self.start_game()

# Main app
root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
