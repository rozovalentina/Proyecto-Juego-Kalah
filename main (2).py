import sys
import copy
import tkinter as tk

class Node:
    def __init__(self, table, next=None, holeMoved=None):
        self.table = table
        self.next = next
        self.holeMoved = holeMoved
        self.heuristic = 0
def createTree(table):
	"""
    Crea el árbol de movimientos para la inteligencia artificial.
  """
	print("IA Jugando")
	root = Node(table)
	points = 0
	minimum = sys.maxsize
	maximum = -sys.maxsize
	holeSelected = None

class Game:
    def __init__(self, players):
        self.players = players
        self.current_player = 0
        self.table = self.start_table()
        self.points = [0] * len(players)

    def start_table(self):
        """
        Inicializa el tablero del juego con 4 semillas en cada hoyo para cada jugador.
        """
        table = [[4 for _ in range(6)] for _ in range(len(self.players))]
        return table

    def movement(self, hole):
        """
        Realiza un movimiento en el juego, moviendo las semillas del hoyo seleccionado.
        """
        is_ai = self.players[self.current_player] == "AI"
        another_move = False
        balls_left = self.table[self.current_player][hole]
        limit = 5
        start_in = hole + 1
        last_move_hole = [-1, -1]

        if is_ai:
            limit = 0
            balls_left = self.table[self.current_player][hole]
            self.table[self.current_player][hole] = 0
            start_in = hole - 1
        else:
            self.table[self.current_player][hole] = 0

        while balls_left > 0:
            if is_ai:
                if limit == 5:
                    for i in range(limit + 1):
                        if balls_left > 0:
                            self.table[1][i] += 1
                            balls_left -= 1
                    last_move_hole = [-1, -1]
                    limit = 0
                else:
                    for i in range(start_in, limit - 1, -1):
                        if balls_left > 0:
                            self.table[0][i] += 1
                            balls_left -= 1
                            last_move_hole = [0, i]
                    if balls_left > 0:
                        self.points[0] += 1
                        if balls_left == 1 and last_move_hole[1] == 0:
                            another_move = True
                        balls_left -= 1
                    limit = 5
                    start_in = 5
            else:
                if limit == 5:
                    for i in range(start_in, limit + 1):
                        if balls_left > 0:
                            self.table[1][i] += 1
                            balls_left -= 1
                            last_move_hole = [1, i]
                    if balls_left > 0:
                        self.points[1] += 1
                        if balls_left == 1 and last_move_hole[1] == 5:
                            another_move = True
                        balls_left -= 1
                    limit = 0
                    start_in = 0
                else:
                    for i in range(5, limit - 1, -1):
                        if balls_left > 0:
                            self.table[0][i] += 1
                            balls_left -= 1
                    last_move_hole = [-1, -1]
                    limit = 5

        if last_move_hole[0] != -1 and last_move_hole[1] != -1 and self.table[last_move_hole[0]][last_move_hole[1]] == 1:
            if last_move_hole[0] == 0:
                self.points[0] += self.table[last_move_hole[0]][last_move_hole[1]] + self.table[1][last_move_hole[1]]
                self.table[last_move_hole[0]][last_move_hole[1]] = 0
                self.table[1][last_move_hole[1]] = 0
            else:
                self.points[1] += self.table[last_move_hole[0]][last_move_hole[1]] + self.table[0][last_move_hole[1]]
                self.table[last_move_hole[0]][last_move_hole[1]] = 0
                self.table[0][last_move_hole[1]] = 0

        return another_move

    def check_game_over(self):
        """
        Verifica si el juego ha terminado.
        """
        for i in range(len(self.players)):
            has_movements = False
            for j in range(6):
                if self.table[i][j] != 0:
                    has_movements = True
                    break
            if not has_movements:							  
                self.points[i] += sum(self.table[i])

        return all(self.table[i][j] == 0 for i in range(len(self.players)) for j in range(6))

    def make_move(self, is_ai, hole):
        """
        Realiza un movimiento en el juego, ya sea del jugador o de la IA.
        """
        if self.players[self.current_player] != "AI" and is_ai:
            return

        if self.table[self.current_player][hole] == 0:
            return

        another_move = self.movement(hole)

        if not another_move:
            self.current_player = (self.current_player + 1) % len(self.players)

        self.check_game_over()

    def ai_move(self):
        """
        Realiza un movimiento de la IA.
        """
        table_copy = copy.deepcopy(self.table)
        selected_hole = createTree(table_copy)
        if selected_hole is not None:
            self.make_move(False, selected_hole)
        return selected_hole

    def get_winner(self):
        """
        Obtiene los índices de los jugadores ganadores según sus puntos.
        """
        max_points = max(self.points)
        winners = [i for i, p in enumerate(self.points) if p == max_points]
        return winners


class GUI:
    def __init__(self, root, players):
        self.root = root
        self.players = players
        self.game = Game(players)

        self.root.title("Mancala Game")
        self.root.geometry("500x300")

        self.label_title = tk.Label(root, text="Mancala Game", font=("Arial", 18))
        self.label_title.pack(pady=10)

        self.frame_board = tk.Frame(root)
        self.frame_board.pack()

        self.labels_holes = []
        for i in range(len(self.players)):
            for j in range(6):
                label = tk.Label(self.frame_board, text="4", font=("Arial", 16), width=3, relief="solid")
                label.grid(row=i, column=j, padx=5, pady=5)
                self.labels_holes.append(label)

        self.frame_buttons = tk.Frame(root)
        self.frame_buttons.pack(pady=10)

        self.buttons_holes = []
        for i in range(6):
            button = tk.Button(self.frame_buttons, text=str(i+1), font=("Arial", 12), width=3, command=lambda idx=i: self.move(idx))
            button.grid(row=0, column=i, padx=5, pady=5)
            self.buttons_holes.append(button)

        self.label_result = tk.Label(root, text="", font=("Arial", 14))
        self.label_result.pack(pady=10)

        self.update_board()

    def move(self, hole):
        """
        Maneja el movimiento del jugador.
        """
        if self.players[self.game.current_player] == "Player":
            if self.game.table[self.game.current_player][hole] != 0:
                another_move = self.game.movement(hole)
                self.update_board()

                if not another_move:
                    self.game.current_player = (self.game.current_player + 1) % len(self.players)
                    if self.players[self.game.current_player] == "AI":
                        self.ai_move()

                if self.game.check_game_over():
                    winners = self.game.get_winner()
                    if len(winners) == 1:
                        self.label_result.config(text=f"Player {winners[0]+1} wins!")
                    else:
                        self.label_result.config(text="It's a tie!")
                    for button in self.buttons_holes:
                        button.config(state="disabled")
                else:
                    self.update_board()
        else:
            return

    def ai_move(self):
        """
        Realiza un movimiento de la IA.
        """
        hole = self.game.ai_move()
        self.update_board()

        if self.game.check_game_over():
            winners = self.game.get_winner()
            if len(winners) == 1:
                self.label_result.config(text=f"Player {winners[0]+1} wins!")
            else:
                self.label_result.config(text="It's a tie!")
            for button in self.buttons_holes:
                button.config(state="disabled")
        else:
            self.game.current_player = (self.game.current_player + 1) % len(self.players)

    def update_board(self):
        """
        Actualiza la visualización del tablero.
        """
        for i in range(len(self.players)):
            for j in range(6):
                self.labels_holes[i*6+j].config(text=str(self.game.table[i][j]))

def main():
    root = tk.Tk()
    players = ["Player", "AI"]
    gui = GUI(root, players)
    root.mainloop()

if __name__ == '__main__':
    main()





