def save(user, game):
    game.save()
    user.game_played += 1
    user.experience += int(game.score)
    if user.highest_score is None:
        highest_score = 0
    else:
        highest_score = user.highest_score
    user.highest_score = max(highest_score, int(game.score))
    user.save()


def validate(game):
    return True
