import tkinter as tk
from tkinter import messagebox  # Ajout de l'importation manquante
import random

class Checkerboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Dames")
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.populate_board()
        self.selected_piece = None
        self.current_player = 'B'
        self.label_turn = tk.Label(self.master, text=f"Tour du joueur {self.current_player}")
        self.label_turn.pack()
        self.create_board_gui()

    def populate_board(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.board[i][j] = 'B'
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.board[i][j] = 'W'

    def create_board_gui(self):
        self.buttons = [[None for _ in range(8)] for _ in range(8)]

        for i in range(8):
            for j in range(8):
                color = 'white' if (i + j) % 2 == 0 else 'black'
                self.buttons[i][j] = tk.Button(self.master, text=self.board[i][j], width=5, height=2,
                                               command=lambda row=i, col=j: self.on_button_click(row, col, color))
                self.buttons[i][j].pack(row=i, column=j)
                self.buttons[i][j].config(bg=color)

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                x1, y1 = j * 50, i * 50
                x2, y2 = x1 + 50, y1 + 50
                color = "white" if (i + j) % 2 == 0 else "black"
                self.buttons[i][j].config(text=self.board[i][j], bg=color)
                self.master.update()

    def handle_click(self, event):
        row, col = event.y // 50, event.x // 50
        if self.selected_piece is None:
            self.selected_piece = (row, col)
        else:
            dest = (row, col)
            if self.is_valid_move(self.selected_piece, dest):
                self.make_move(self.selected_piece, dest)
                self.selected_piece = None
                self.draw_board()
                if self.is_game_over():
                    self.end_game(self.current_player)
                else:
                    self.switch_player()
                    self.computer_move()
                    self.draw_board()
                    if self.is_game_over():
                        self.end_game('B' if self.current_player == 'W' else 'W')

    def is_valid_move(self, start, end):
        row_start, col_start = start
        row_end, col_end = end
    
        is_simple_move = (
            0 <= row_start < 8 and
            0 <= col_start < 8 and
            0 <= row_end < 8 and
            0 <= col_end < 8 and
            self.board[row_start][col_start] != ' ' and
            self.board[row_end][col_end] == ' ' and
            abs(row_end - row_start) == 1 and
            abs(col_end - col_start) == 1
        )
    
        if is_simple_move:
            return True
        else:
            is_capture_move = (
                0 <= row_start < 8 and
                0 <= col_start < 8 and
                0 <= row_end < 8 and
                0 <= col_end < 8 and
                self.board[row_start][col_start] != ' ' and
                self.board[row_end][col_end] == ' ' and
                abs(row_end - row_start) == 2 and
                abs(col_end - col_start) == 2
            )
    
            if is_capture_move:
                mid_row = (row_start + row_end) // 2
                mid_col = (col_start + col_end) // 2
    
                if self.board[mid_row][mid_col] != ' ' and self.board[mid_row][mid_col] != self.board[row_start][col_start]:
                    self.board[mid_row][mid_col] = ' '
                    return True
    
            print("Mouvement invalide !")
            return False

    def make_move(self, start, end):
        row_start, col_start = start
        row_end, col_end = end
        self.board[row_end][col_end] = self.board[row_start][col_start]
        self.board[row_start][col_start] = ' '

        # Si une pièce atteint la dernière rangée, elle devient une dame
        if self.board[row_end][col_end] == 'B' and row_end == 7:
            self.board[row_end][col_end] = 'BK'
        elif self.board[row_end][col_end] == 'W' and row_end == 0:
            self.board[row_end][col_end] = 'WK'

    def switch_player(self):
        self.current_player = 'W' if self.current_player == 'B' else 'B'
        self.label_turn.config(text=f"Tour du joueur {self.current_player}")

    def end_game(self, winner):
        messagebox.showinfo("Fin de partie", f"Le joueur {winner} a gagné!")
        self.master.quit()  # Correction : Utilisez self.master.quit() au lieu de self.master.destroy()

    def computer_move(self):
        valid_pieces = [(i, j) for i in range(8) for j in range(8) if self.board[i][j] == 'B' and self.get_possible_moves((i, j))]
    
        if valid_pieces:
            selected_piece = random.choice(valid_pieces)
            possible_moves = self.get_possible_moves(selected_piece)
            move = random.choice(possible_moves)
            self.make_move(selected_piece, move)

    def get_possible_moves(self, piece):
        row, col = piece
        possible_moves = []
    
        for i in range(row - 1, row + 2, 2):
            for j in range(col - 1, col + 2, 2):
                if 0 <= i < 8 and 0 <= j < 8 and self.board[i][j] == ' ':
                    possible_moves.append((i, j))
                elif 0 <= i < 8 and 0 <= j < 8 and self.board[i][j] != ' ' and self.board[i][j] != self.board[row][col]:
                    new_row = i + (i - row)
                    new_col = j + (j - col)
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row][new_col] == ' ':
                        possible_moves.append((new_row, new_col))
    
        return possible_moves

    def is_game_over(self):
        # Vérifie si l'un des joueurs n'a plus de pièces à jouer
        return not any(self.get_possible_moves((i, j)) for i in range(8) for j in range(8) if self.board[i][j] == 'B') or \
               not any(self.get_possible_moves((i, j)) for i in range(8) for j in range(8) if self.board[i][j] == 'W')


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    checkerboard = Checkerboard(root)
    root.mainloop()
