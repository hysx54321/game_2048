import json


# up down left right
# merge
# move to left
# rotate reflect
# test new number 2/4

# stretch goal: random seed

def is_valid_board(board):
    if len(board) != 4:
        return False
    for i in range(4):
        if len(board[i]) != 4:
            return False
    return True


def is_valid_start(state):
    if state['score'] != 0:
        return False
    if state['previousMove'] is not None:
        return False
    count = 0
    board = state['board']
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                if board[i][j] != 2 and board[i][j] != 4:
                    return False
                count += 1

    return count == 1


def save(user, game):
    game.save()
    user.game_played += 1
    user.experience += int(game.score)
    if user.highest_score is None:
        highest_score = 0
    else:
        highest_score = user.highest_score
    user.highest_score = max(highest_score, int(game.score))
    user.best_game = game
    user.save()


def validate(game):
    try:
        history = json.loads(game.game_reconstruction)
    except:
        return False

    if int(game.move) + 1 != len(history):
        return False

    if int(game.score) != history[len(history) - 1]['score']:
        return False

    for i in range(len(history)):
        if not is_valid_board(history[i]['board']):
            return False

    if not is_valid_start(history[0]):
        return False

    return True
