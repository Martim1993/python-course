class User:
    def __init__(self, name1: str, name2: str):
        self.name1 = name1
        self.name2 = name2


class Play:
    def __init__(self, user):
        self.board = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        self.current_player = user.name1
        self.score = {user.name1: 0, user.name2: 0}

    def print_board(self):
        for row in self.board:
            print(f"{row}")

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        if all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            return 'Draw'

    def make_move(self, row, col):
        if self.board[row][col] != ' ':
            raise ValueError("Эта клетка уже занята!")
        if self.current_player == user.name2:
            self.board[row][col] = 'O'
            self.current_player = user.name1

        elif self.current_player == user.name1:
            self.board[row][col] = 'X'
            self.current_player = user.name2

    def reset_board(self):
        self.board = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        self.current_player = user.name1

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
                    if winner == 'X':
                        print(f"Игрок {user.name1} выиграл раунд!")
                        self.score[user.name1] += 1
                    else:
                        print(f"Игрок {user.name2} выиграл раунд!")
                        self.score[user.name2] += 1
                break

    def play_game(self):
        print("Добро пожаловать в игру Крестики-нолики!")
        for round_num in range(1, 4):
            print(f"\nРаунд {round_num}")
            self.play_round()
            print(f"Счет: {user.name1} - {self.score[user.name1]}, {user.name2} - {self.score[user.name2]}")

        print("\nИгра завершена!")
        if self.score[user.name1] > self.score[user.name2]:
            print(f"Игрок {user.name1} выиграл игру!")
        elif self.score[user.name2] > self.score[user.name1]:
            print(f"Игрок {user.name2} выиграл игру!")
        else:
            print("Ничья по итогам игры!")


user = User('Mar', 'Tim')
game = Play(user)
game.play_game()
