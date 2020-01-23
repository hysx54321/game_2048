import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from two_zero_four_eight.forms import SaveGameForm
from .models import Game, User


@login_required
def save_game_fake(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SaveGameForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            game = Game()
            game.duration_second = (timezone.now() - game.started_at).seconds * 1000000000
            game.player = request.user
            game.score = form.cleaned_data['magic_number']
            game.move = 24 * game.score
            game.game_reconstruction = str(game.score) + ',' + str(2 * game.score)
            game.save()

            user = User.objects.filter(id=request.user.id)[0]
            user.game_played += 1
            user.experience += game.score
            user.highest_score = max(request.user.highest_score, game.score)
            user.save()

            messages.add_message(request, messages.INFO,
                                 'Successfully played a game with score ' + str(game.score))

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('play-game'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = SaveGameForm(initial={'magic_number': 888})

    context = {
        'form': form,
    }

    return render(request, 'two_zero_four_eight/play_game.html', context)


@login_required
def save_game(request):
    if request.method == 'POST':
        game = Game()
        game.duration_second = request.POST['second']
        game.player = request.user
        game.score = request.POST['score'];
        game.move = request.POST['move'];
        game.game_reconstruction = request.POST['reconstruction'];
        game.save()

        user = User.objects.filter(id=request.user.id)[0]
        user.game_played += 1
        user.experience += int(game.score)
        user.highest_score = max(request.user.highest_score, int(game.score))
        user.save()

        messages.add_message(request, messages.INFO,
                             'Successfully saved a game with score ' + str(game.score))
        return HttpResponseRedirect(reverse('game-detail', kwargs={'pk': game.pk}))
    else:
        return HttpResponseRedirect(reverse('user-game', kwargs={'user_id': request.user.id}))


@login_required
def play_game(request):
    return render(request, 'two_zero_four_eight/play_game_real.html')
