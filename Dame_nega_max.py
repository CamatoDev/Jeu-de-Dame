# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 21:04:49 2023

@author: Camato & Kamto
"""

import tkinter as tk
import random

class Checkerboard:
    def __init__(self, master):
        # Initialisation de la classe Checkerboard
        self.master = master
        self.master.title("Dames")
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.populate_board()
        self.selected_piece = None

        # Configuration et création de la fenêtre Tkinter
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg='white')
        self.canvas.pack()
        self.draw_board()

        # Liaison de la fonction handle_click à l'événement clic de la souris
        self.canvas.bind("<Button-1>", self.handle_click)
        
        #ajout
        self.current_player = 'B'  # 'B' pour les noirs, 'W' pour les blancs
        self.label_turn = tk.Label(self.master, text=f"Tour du joueur {self.current_player}")
        self.label_turn.pack()
    
        #ajout 
    def switch_player(self):
        # Passe au joueur suivant
        self.current_player = 'W' if self.current_player == 'B' else 'B'
        self.label_turn.config(text=f"Tour du joueur {self.current_player}")

    def end_game(self, winner=None):
        # Affiche un message de fin de partie
        if winner:
            tk.messagebox.showinfo("Fin de partie", f"Le joueur {winner} a gagné!")
        else:
            tk.messagebox.showinfo("Fin de partie", "Match nul!")
        self.master.destroy()
    #fin ajout 

    def populate_board(self):
        # Initialisation du tableau du jeu de dames avec les pièces
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.board[i][j] = 'B'
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.board[i][j] = 'W'

    def draw_board(self):
        # Dessine le plateau de jeu sur le canevas Tkinter
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x1, y1 = j * 50, i * 50
                x2, y2 = x1 + 50, y1 + 50
                color = "white" if (i + j) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                # Nouvelle apparence pour les pions couronnés
                if self.board[i][j] == 'BK':
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="black", outline="white", width=2)
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text='K', font=('Arial', 12, 'bold'), fill='white')
                elif self.board[i][j] == 'WK':
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="white", outline="black", width=2)
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text='K', font=('Arial', 12, 'bold'), fill='black')
                else:
                    # Ancienne apparence pour les pions normaux
                    if self.board[i][j] == 'B':
                        self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="brown", outline="black")
                    elif self.board[i][j] == 'W':
                        self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="grey", outline="white")


    def handle_click(self, event):
        #ajout
        if self.is_game_over():
            self.end_game()
        # Gère l'événement clic de la souris
        row, col = event.y // 50, event.x // 50
        if self.selected_piece is None:
            self.selected_piece = (row, col)
        else:
            dest = (row, col)
            if self.is_valid_move(self.selected_piece, dest):
                self.make_move(self.selected_piece, dest)
                self.selected_piece = None
                self.draw_board()
                self.computer_move()
                self.draw_board()
            else :
                self.selected_piece = None

    def is_valid_move(self, start, end):
        # Vérifie si le mouvement est valide
        row_start, col_start = start
        row_end, col_end = end
    
        # Conditions principales pour un mouvement simple
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
            # Conditions pour une prise multiple
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
                # Conditions supplémentaires pour la prise multiple
                # (à adapter selon les règles spécifiques du jeu)
                mid_row = (row_start + row_end) // 2
                mid_col = (col_start + col_end) // 2
    
                if self.board[mid_row][mid_col] != ' ' and self.board[mid_row][mid_col] != self.board[row_start][col_start]:
                    self.board[mid_row][mid_col] = ' '
                    return True
    
            # Si aucune condition n'est satisfaite, le mouvement n'est pas valide
            print("Mouvement invalide !")
            return False


    def make_move(self, start, end):
        # Effectue le mouvement
        row_start, col_start = start
        row_end, col_end = end
        self.board[row_end][col_end] = self.board[row_start][col_start]
        self.board[row_start][col_start] = ' '
        #ajout 
        self.promote_to_king(end[0], end[1])  # Vérifie si la pièce doit être couronnée
        self.switch_player()  # Passe au joueur suivant après chaque mouvement

    def computer_move(self, depth=3):
        # Obtient une liste de toutes les pièces noires qui peuvent effectuer des mouvements valides
        valid_pieces = [(i, j) for i in range(8) for j in range(8) if self.board[i][j] == 'B' and self.get_possible_moves((i, j))]
    
        if valid_pieces and depth > 0:
            # Choisit au hasard une pièce parmi celles qui peuvent effectuer des mouvements valides
            selected_piece = random.choice(valid_pieces)
    
            # Obtient tous les mouvements possibles pour la pièce sélectionnée
            possible_capture_moves = self.get_capture_moves(selected_piece)
    
            if possible_capture_moves:
                # Choix au hasard d'une capture parmi les captures possibles
                move = random.choice(possible_capture_moves)
                # Effectue le mouvement
                self.make_move(selected_piece, move)
                # Vérifie la promotion après le déplacement
                self.promote_to_king(move[0], move[1])
                # Supprime la pièce capturée
                self.remove_captured_piece(selected_piece, move)
                # Met à jour l'affichage
                self.draw_board()
    
                # Appel récursif pour évaluer le score
                score = -self.nega_max(depth - 1)
    
                # Annule le mouvement pour revenir à l'état précédent
                self.undo_move(selected_piece, move)
                # Met à jour l'affichage après l'annulation
                self.draw_board()
    
                return score
    
            else:
                # Aucune capture possible, choisi un mouvement simple
                possible_moves = self.get_possible_moves(selected_piece)
                scores = []
    
                for move in possible_moves:
                    # Effectue le mouvement
                    self.make_move(selected_piece, move)
                    # Vérifie la promotion après le déplacement
                    self.promote_to_king(move[0], move[1])
                    # Met à jour l'affichage
                    self.draw_board()
    
                    # Appel récursif pour évaluer le score
                    score = -self.nega_max(depth - 1)
                    scores.append(score)
    
                    # Annule le mouvement pour revenir à l'état précédent
                    self.undo_move(selected_piece, move)
                    # Met à jour l'affichage après l'annulation
                    self.draw_board()
    
                # Retourne le score maximal trouvé parmi les mouvements possibles
                return max(scores)
    
        return 0
    
    def nega_max(self, depth):
        # Fonction NegaMax utilisée pour évaluer le score des positions
        if depth == 0 or self.is_game_over():
            # Évaluation de la position actuelle
            return self.evaluate_position()
    
        # Obtient une liste de toutes les pièces noires qui peuvent effectuer des mouvements valides
        valid_pieces = [(i, j) for i in range(8) for j in range(8) if self.board[i][j] == 'B' and self.get_possible_moves((i, j))]
    
        scores = []
    
        for piece in valid_pieces:
            # Obtient tous les mouvements possibles pour la pièce sélectionnée
            possible_moves = self.get_possible_moves(piece)
    
            for move in possible_moves:
                # Effectue le mouvement
                self.make_move(piece, move)
                # Vérifie la promotion après le déplacement
                self.promote_to_king(move[0], move[1])
                # Met à jour l'affichage
                self.draw_board()
    
                # Appel récursif pour évaluer le score
                score = -self.nega_max(depth - 1)
                scores.append(score)
    
                # Annule le mouvement pour revenir à l'état précédent
                self.undo_move(piece, move)
                # Met à jour l'affichage après l'annulation
                self.draw_board()
    
        # Retourne le score maximal trouvé parmi les mouvements possibles
        return max(scores)
    
    def evaluate_position(self):
        # Fonction d'évaluation de la position
        score = 0
    
        # Parcourez le plateau pour attribuer des points en fonction de la position des pièces
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece == 'B':
                    # Ajoute des points pour chaque pion noir
                    score += 1
                elif piece == 'BK':
                    # Ajoute plus de points pour chaque dame noire
                    score += 3
                elif piece == 'W':
                    # Soustrait des points pour chaque pion blanc
                    score -= 1
                elif piece == 'WK':
                    # Soustrait plus de points pour chaque dame blanche
                    score -= 3
    
        return score


    
    
    def remove_captured_piece(self, start, end):
        # Calcul des coordonnées de la pièce capturée
        captured_row = (start[0] + end[0]) // 2
        captured_col = (start[1] + end[1]) // 2
        # Supprime la pièce capturée du plateau
        self.board[captured_row][captured_col] = ' '


    def get_simple_moves(self, piece):
        # Décomposition des coordonnées de la pièce
        row, col = piece
        # Initialisation de la liste des mouvements possibles
        possible_moves = []
    
        # Parcours des cases diagonales
        for i in range(row - 1, row + 2, 2):
            for j in range(col - 1, col + 2, 2):
                # Vérifie que la case est à l'intérieur du plateau et vide
                if 0 <= i < 8 and 0 <= j < 8 and self.board[i][j] == ' ':
                    possible_moves.append((i, j))
    
        return possible_moves

    def get_capture_moves(self, piece):
        # Décomposition des coordonnées de la pièce
        row, col = piece
        # Initialisation de la liste des mouvements possibles
        possible_moves = []
    
        # Parcours des cases diagonales
        for i in range(row - 1, row + 2, 2):
            for j in range(col - 1, col + 2, 2):
                # Vérifie que la case est à l'intérieur du plateau
                if 0 <= i < 8 and 0 <= j < 8 and self.board[i][j] != ' ' and self.board[i][j] != self.board[row][col]:
                    # Calcul des coordonnées de la case adjacente à la pièce adverse
                    new_row = i + (i - row)
                    new_col = j + (j - col)
                    # Vérifie que la case adjacente à la pièce adverse est vide
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row][new_col] == ' ':
                        # Ajoute la case adjacente vide à la liste des mouvements possibles
                        possible_moves.append((new_row, new_col))

        return possible_moves
    
    # Dans la méthode principale
    def get_possible_moves(self, piece):
        # Utilisez les nouvelles fonctions pour obtenir les mouvements possibles
        possible_moves_simple = self.get_simple_moves(piece)
        possible_moves_capture = self.get_capture_moves(piece)
        
        # Retourne la liste des mouvements possibles
        return possible_moves_simple + possible_moves_capture
    
    def is_game_over(self):
        # Compte le nombre de pièces restantes pour chaque joueur
        count_black_pieces = sum(row.count('B') + row.count('BK') for row in self.board)
        count_white_pieces = sum(row.count('W') + row.count('WK') for row in self.board)
    
        # Vérifie si l'un des joueurs n'a plus de pièces
        if count_black_pieces == 0:
            self.end_game(winner='W')  # Les pièces blanches ont gagné
            return True
        elif count_white_pieces == 0:
            self.end_game(winner='B')  # Les pièces noires ont gagné
            return True
    
        return False  # La partie n'est pas terminée
    
    #ajout
    def promote_to_king(self, row, col):
        # Couronne une pièce en dame
        if self.current_player == 'B' and row == 0:
            self.board[row][col] = 'WK'  # 'BK' représente une dame noire
        elif self.current_player == 'W' and row == 7:
            self.board[row][col] = 'BK'  # 'WK' représente une dame blanche
    



if __name__ == "__main__":
    # Initialisation et exécution du programme Tkinter
    root = tk.Tk()
    root.resizable(width=False, height=False)
    checkerboard = Checkerboard(root)
    root.mainloop()
