import os;
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")  # NoQA
import django;

django.setup()
from two_zero_four_eight.models import User, Game, Follow

# create 10 test users
for i in range(10):
    other_users = User.objects.all()
    new_user = User.objects.create_user(username="testuser" + str(i), password="test")
    for user in other_users:
        if random.random() > 0.5:
            follow = Follow()
            follow.follower = new_user
            follow.user = user
            follow.save()

player = User.objects.create_user(username="player1", password="player")
game = Game()
game.duration_second = 123
game.player = player
game.score = 10
game.move = 2
game.game_reconstruction = '[{"board":[[0,0,0,0],[0,0,0,0],[2,0,0,0],[0,0,0,0]],"score":0,"previousMove":null},' \
                           '{"board":[[0,0,2,0],[0,0,0,0],[0,0,0,0],[2,0,0,0]],"score":0,"previousMove":2}] '
game.save()
