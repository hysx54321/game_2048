from django.urls import path, include
from . import views, follow_manager, game_manager

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('user_rank/', views.RankListView.as_view(), name='user-rank'),
    path('user_following/', views.UserFollowingListView.as_view(), name='user-following'),
    path('user_follower/', views.UserFollowerListView.as_view(), name='user-follower'),
    path('user/<int:user_id>/games', views.UserGameListView.as_view(), name='user-game'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='game-detail'),
    path('game_replay/<int:game_id>', game_manager.replay_game, name='game-replay'),
    path('save_game/', game_manager.save_game, name='save-game'),
    path('play/', game_manager.play_game, name='play-game'),
    path('add_follow/', follow_manager.add_follow, name='add-follow'),
    path('remove_follow/', follow_manager.remove_follow, name='remove-follow'),
]
