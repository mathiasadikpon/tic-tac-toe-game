import tkinter as tk
from tkinter import messagebox
from TicTacToe import TicTacToe
from ButtonCustom import ButtonCustom

class Driver:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - MVC Style")

        self.player1_name = tk.StringVar(value="X")
        self.player2_name = tk.StringVar(value="O")
        self.board_size = tk.IntVar(value=3)
        self.buttons = []
        self.game = None

        self.setup_ui()
        self.configure_grid()

    def setup_ui(self):
        tk.Label(self.root, text="Player X:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.player1_name).grid(row=0, column=1, sticky="ew")

        tk.Label(self.root, text="Player O:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.player2_name).grid(row=1, column=1, sticky="ew")

        tk.Label(self.root, text="Board Size:").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.board_size).grid(row=2, column=1, sticky="ew")

        self.start_btn = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_btn.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="nsew")

        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")

        self.restart_btn = tk.Button(self.root, text="Restart", command=self.start_game, state="disabled")
        self.restart_btn.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=5)

    def configure_grid(self):
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)

    def start_game(self):
        size = self.board_size.get()
        if size < 3 or size > 10:
            messagebox.showwarning("Invalid size", "Board size must be between 3 and 10")
            return

        self.game = TicTacToe(size)
        self.status_label.config(text=f"{self.player1_name.get()}'s turn (X)")
        self.restart_btn.config(state="normal")

        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.buttons.clear()

        for i in range(size):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

        for i in range(size * size):
            btn = ButtonCustom(self.board_frame, i, self.handle_click)
            btn.grid(row=i // size, column=i % size, sticky="nsew")
            self.buttons.append(btn)

    def handle_click(self, index):
        if not self.game.make_move(index):
            return

        symbol = self.game.current_player
        self.buttons[index].set_symbol(symbol)

        if self.game.check_winner():
            name = self.player1_name.get() if symbol == "X" else self.player2_name.get()
            self.status_label.config(text=f"{name} wins!")
            messagebox.showinfo("Game Over", f"{name} ({symbol}) wins!")
            self.disable_board()
            return

        if self.game.is_draw():
            self.status_label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            self.disable_board()
            return

        self.game.switch_player()
        next_player = self.player1_name.get() if self.game.current_player == "X" else self.player2_name.get()
        self.status_label.config(text=f"{next_player}'s turn ({self.game.current_player})")

    def disable_board(self):
        for btn in self.buttons:
            btn.unbind("<Button-1>")

# Main run
if __name__ == "__main__":
    root = tk.Tk()
    Driver(root)
    root.mainloop()
