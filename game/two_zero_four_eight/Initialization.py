import os;
import random

from two_zero_four_eight.follow_manager import save as save_follow

from two_zero_four_eight.game_manager import save as save_game

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")  # NoQA
import django;

django.setup()
from two_zero_four_eight.models import User, Game, Follow

admin = User.objects.create_user(username="admin", password="Sty971118!", is_staff=True, is_superuser=True)
syx = User.objects.create_user(username="shyx54321", password="shen960915")

# create 10 test users
for i in range(10):
    other_users = User.objects.all()
    new_user = User.objects.create_user(username="testuser" + str(i), password="test")
    for user in other_users:
        if random.random() > 0.5:
            follow = Follow()
            follow.follower = new_user
            follow.user = user
            save_follow(follow)

    num_game = random.randint(0, 10)
    for j in range(num_game):
        game = Game()
        game.duration_second = random.randint(1, 100)
        game.player = new_user
        game.score = random.randint(10, 1000)
        game.move = random.randint(1, 100)
        game.game_reconstruction = '[{"board":[[0,0,0,0],[0,0,0,0],[2,0,0,0],[0,0,0,0]],"score":0,"previousMove":null},' \
                                   '{"board":[[0,0,2,0],[0,0,0,0],[0,0,0,0],[2,0,0,0]],"score":0,"previousMove":2}] '
        save_game(new_user, game)
