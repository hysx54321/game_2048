import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from two_zero_four_eight.forms import SaveGameForm
from .game_manager import save, validate
from .models import Game, User


@login_required
def save_game(request):
    if request.method == 'POST':
        game = Game()
        game.duration_second = request.POST['second']
        game.player = request.user
        game.score = request.POST['score']
        game.move = request.POST['move']
        game.useless_move = request.POST['useless_move']
        game.game_reconstruction = request.POST['reconstruction']
        if not validate(game):
            return HttpResponseRedirect(reverse('user-game', kwargs={'user_id': request.user.id}))
        save(request.user, game)

        messages.add_message(request, messages.INFO,
                             'Successfully saved a game with score ' + str(game.score))
        return HttpResponseRedirect(reverse('game-detail', kwargs={'pk': game.pk}))
    else:
        return HttpResponseRedirect(reverse('user-game', kwargs={'user_id': request.user.id}))


@login_required
def play_game(request):
    return render(request, 'two_zero_four_eight/play_game_real.html')


def replay_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render(request, 'two_zero_four_eight/game_replayer.html', context={"game": game})
