class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.score = {'X': 0, 'O': 0}

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def check_winner(self):
        # Проверка строк
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]

        # Проверка столбцов
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        # Проверка диагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        # Проверка на ничью
        if all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            return 'Draw'

        return None

    def make_move(self, row, col):
        if self.board[row][col] != ' ':
            raise ValueError("Эта клетка уже занята!")
        self.board[row][col] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def play_round(self):
        self.reset_board()
        while True:
            self.print_board()
            try:
                row, col = map(int, input(f"Игрок {self.current_player}, введите строку и столбец (0, 1, 2): ").split())
                if row not in range(3) or col not in range(3):
                    raise ValueError("Некорректные координаты!")
                self.make_move(row, col)
            except ValueError as e:
                print(e)
                continue

            winner = self.check_winner()
            if winner:
                self.print_board()
                if winner == 'Draw':
                    print("Ничья!")
                else:
                    print(f"Игрок {winner} выиграл раунд!")
                    self.score[winner] += 1
                break

    def play_game(self):
        print("Добро пожаловать в игру Крестики-нолики!")
        for round_num in range(1, 4):
            print(f"\nРаунд {round_num}")
            self.play_round()
            print(f"Счет: X - {self.score['X']}, O - {self.score['O']}")

        print("\nИгра завершена!")
        if self.score['X'] > self.score['O']:
            print("Игрок X выиграл игру!")
        elif self.score['O'] > self.score['X']:
            print("Игрок O выиграл игру!")
        else:
            print("Ничья по итогам игры!")

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()