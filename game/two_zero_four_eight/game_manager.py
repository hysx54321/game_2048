import json


# up down left right
# merge
# move to left
# rotate reflect
# test new number 2/4

# stretch goal: random seed

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
    return True
