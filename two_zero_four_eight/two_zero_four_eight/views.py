from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from two_zero_four_eight.models import User, Game, Follow
from django.contrib.auth.decorators import login_required


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_users = User.objects.all().count()
    num_games = Game.objects.all().count()

    context = {
        'num_users': num_users,
        'num_games': num_games,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required
def play(request):
    context = {
        'num_users': 0,
        'num_games': 0,
    }
    return render(request, 'two_zero_four_eight/play_game.html', context=context)


class UserListView(generic.ListView):
    model = User
    paginate_by = 5


class RankListView(generic.ListView):
    model = User
    paginate_by = 5
    ordering = ['-highest_score']
    template_name = 'two_zero_four_eight/user_rank_list.html'

    def get_queryset(self):
        return User.objects.filter(highest_score__isnull=False)


class UserDetailView(generic.DetailView):
    model = User
    context_object_name = 'user_detail'


class GameListView(generic.ListView):
    model = Game
    paginate_by = 5


class GameDetailView(generic.DetailView):
    model = Game


class UserFollowingListView(LoginRequiredMixin, generic.ListView):
    #model = Follow
    paginate_by = 5
    template_name = 'two_zero_four_eight/user_following_list.html'

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user, active=True)


class UserFollowerListView(LoginRequiredMixin, generic.ListView):
    #model = Follow
    paginate_by = 5
    template_name = 'two_zero_four_eight/user_follower_list.html'

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user, active=True)


class UserGameListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = 'two_zero_four_eight/user_game_list.html'
    context_object_name = 'user_game_list'

    def __init__(self):
        super().__init__()
        #self.user = get_object_or_404(User, id=self.kwargs['user_id'])

    def get_queryset(self):
        self.user = get_object_or_404(User, id=self.kwargs['user_id'])
        return Game.objects.filter(player=self.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        #self.user = get_object_or_404(User, id=self.kwargs['user_id'])
        context['player'] = self.user
        return context
