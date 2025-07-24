import tkinter as tk

class ButtonCustom(tk.Canvas):
    def __init__(self, master, index, on_click_callback):
        super().__init__(master, bg="white", highlightthickness=1)
        self.index = index
        self.symbol = None
        self.on_click = on_click_callback
        self.bind("<Button-1>", self.on_click_event)
        self.bind("<Configure>", self.redraw)

    def on_click_event(self, event):
        self.on_click(self.index)

    def set_symbol(self, symbol):
        self.symbol = symbol
        self.redraw()

    def redraw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        self.create_oval(5, 5, w - 5, h - 5, fill="#f0f0f0", outline="black")
        if self.symbol == "X":
            self.create_line(10, 10, w - 10, h - 10, fill="red", width=3)
            self.create_line(w - 10, 10, 10, h - 10, fill="red", width=3)
        elif self.symbol == "O":
            self.create_oval(10, 10, w - 10, h - 10, outline="blue", width=3)
