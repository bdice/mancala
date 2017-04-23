import numpy as np

class NoStonesException(Exception):
    pass

class InvalidMovePitException(Exception):
    pass

def new_board():
    return np.array([4, 4, 4, 4, 4, 4, 0,
                     4, 4, 4, 4, 4, 4, 0], dtype=np.uint8)

def get_player_info():
    p1 = input('First player\'s name: ') or 'AI 1'
    p2 = input('Second player\'s name: ') or 'AI 2'
    return p1, p2

def is_ai(player):
    return player[:2] == 'AI'

def display_board(board, p1, p2, turn, numbered=False):
    print('[{}] {}'.format('*' if turn == 1 else ' ', p2))
    if numbered and turn == 1:
        print('     1  2  3  4  5  6')
    print('[  |{:>2}|{:>2}|{:>2}|{:>2}|{:>2}|{:>2}|  ]'.format(*board[12::-1]))
    print('[{:>2}|--|--|--|--|--|--|{:>2}]'.format(*board[13::-7]))
    print('[  |{:>2}|{:>2}|{:>2}|{:>2}|{:>2}|{:>2}|  ]'.format(*board[:7]))
    if numbered and turn == 0:
        print('     6  5  4  3  2  1')
    print('{:>21} [{}]'.format(p1, '*' if turn == 0 else ' '))

def choose_move(board, turn):
    move_pit = np.random.randint(6) + 1
    while True:
        try:
            validate_move(board, turn, move_pit)
            return move_pit
        except Exception:
            move_pit = np.random.randint(6) + 1

def validate_move(board, turn, move_pit):
    try:
        move_pit = int(move_pit)
        if not(1 <= move_pit <= 6):
            raise InvalidMovePitException
        move_pit = turn * 7 + (6 - move_pit)
        if board[move_pit] <= 0:
            raise NoStonesException
        return move_pit
    except Exception:
        raise

def get_move(board, p1, p2, turn):
    while True:
        if is_ai(p1 if turn == 0 else p2):
            move_pit = choose_move(board, turn)
            print('Move:', move_pit)
        else:
            move_pit = input('Move: ')
        try:
            return validate_move(board, turn, move_pit)
        except NoStonesException:
            print('There are no stones in that pit. Try again.')
        except Exception:
            print('Enter a valid number between 1 and 6. See below for numbers:')
            display_board(board, p1, p2, turn, numbered=True)

def move(board, turn, move_pit):
    stones = board[move_pit]
    board[move_pit] = 0
    opponent_store = ((turn)*int(len(board)/2) - 1) % len(board)
    player_store = ((turn+1)*int(len(board)/2) - 1) % len(board)
    while stones > 0:
        move_pit = (move_pit + 1) % len(board)
        if move_pit != opponent_store:
            board[move_pit] += 1
            stones -= 1
        if stones == 0 and board[move_pit] == 1:
            # Capture from across the board
            opposite_pit = move_pit + 2*(6-move_pit)
            if board[opposite_pit] > 0:
                print(p1 if turn == 0 else p2, 'captured', board[opposite_pit], 'stones!')
                board[player_store] += board[opposite_pit]
                board[opposite_pit] = 0
    if move_pit != player_store:
        turn = 1 - turn
    return board, turn

def finish_game(board, p1, p2, turn):
    p1_stones = np.sum(board[0:6])
    p2_stones = np.sum(board[7:13])
    if (p1_stones == 0) or (p2_stones == 0):
        board[6] += p1_stones
        board[13] += p2_stones
        board[0:6] = 0
        board[7:13] = 0
        display_board(board, p1, p2, -1)
        if board[6] == board[13]:
            print('Tie game! Good work,', p1, 'and', p2)
        else:
            print('Congratulations,', p1 if board[6] > board[13] else p2, 'won!')
        return True
    return False

if __name__ == '__main__':
    p1, p2 = get_player_info()
    board = new_board()
    turn = np.random.randint(2)
    display_board(board, p1, p2, turn)
    while not finish_game(board, p1, p2, turn):
        move_pit = get_move(board, p1, p2, turn)
        board, turn = move(board, turn, move_pit)
        print('\n')
        display_board(board, p1, p2, turn)
