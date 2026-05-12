import random
import tkinter as tk
from tkinter import messagebox

SIZE = 4
CELL_SIZE = 100
PADDING = 10
BACKGROUND_COLOR = "#bbada0"

COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

TEXT_COLORS = {
    2: "#776e65",
    4: "#776e65",
    8: "#f9f6f2",
    16: "#f9f6f2",
    32: "#f9f6f2",
    64: "#f9f6f2",
    128: "#f9f6f2",
    256: "#f9f6f2",
    512: "#f9f6f2",
    1024: "#f9f6f2",
    2048: "#f9f6f2",
}


class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")

        self.canvas = tk.Canvas(
            root,
            width=SIZE * CELL_SIZE + PADDING * 2,
            height=SIZE * CELL_SIZE + PADDING * 2,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.board = [[0] * SIZE for _ in range(SIZE)]

        self.add_new_tile()
        self.add_new_tile()

        self.draw_board()

        self.root.bind("<Key>", self.handle_key)

    def add_new_tile(self):
        empty = [
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
            if self.board[r][c] == 0
        ]

        if not empty:
            return

        r, c = random.choice(empty)
        self.board[r][c] = 2 if random.random() < 0.9 else 4

    def draw_board(self):
        self.canvas.delete("all")

        for r in range(SIZE):
            for c in range(SIZE):
                x1 = c * CELL_SIZE + PADDING
                y1 = r * CELL_SIZE + PADDING
                x2 = x1 + CELL_SIZE - PADDING
                y2 = y1 + CELL_SIZE - PADDING

                value = self.board[r][c]
                color = COLORS.get(value, "#3c3a32")

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=""
                )

                if value != 0:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=str(value),
                        fill=TEXT_COLORS.get(value, "#f9f6f2"),
                        font=("Helvetica", 24, "bold")
                    )

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False

        new_board = []

        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)

            if final != row:
                moved = True

            new_board.append(final)

        self.board = new_board
        return moved

    def reverse(self):
        self.board = [row[::-1] for row in self.board]

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_right(self):
        self.reverse()
        moved = self.move_left()
        self.reverse()
        return moved

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def can_move(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == 0:
                    return True

                if c < SIZE - 1 and self.board[r][c] == self.board[r][c + 1]:
                    return True

                if r < SIZE - 1 and self.board[r][c] == self.board[r + 1][c]:
                    return True

        return False

    def check_win(self):
        for row in self.board:
            if 2048 in row:
                return True
        return False

    def handle_key(self, event):
        key = event.keysym

        moved = False

        if key == "Left":
            moved = self.move_left()
        elif key == "Right":
            moved = self.move_right()
        elif key == "Up":
            moved = self.move_up()
        elif key == "Down":
            moved = self.move_down()

        if moved:
            self.add_new_tile()
            self.draw_board()

            if self.check_win():
                messagebox.showinfo("2048", "你贏了！")

            elif not self.can_move():
                messagebox.showinfo("2048", "遊戲結束！")


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()