from django.urls import path, include
from . import views, follow_manager, game_manager, game_controller, follow_controller

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('user_rank/', views.RankListView.as_view(), name='user-rank'),
    path('user_following/', views.UserFollowingListView.as_view(), name='user-following'),
    path('user_follower/', views.UserFollowerListView.as_view(), name='user-follower'),
    path('user/<int:user_id>/games', views.UserGameListView.as_view(), name='user-game'),
    path('new_user/', views.new_user, name='new-user'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='game-detail'),
    path('save_game/', game_controller.save_game, name='save-game'),
    path('play/', game_controller.play_game, name='play-game'),
    path('add_follow/', follow_controller.add_follow, name='add-follow'),
    path('remove_follow/', follow_controller.remove_follow, name='remove-follow'),
    path('remove_follower/', follow_controller.remove_follower, name='remove-follower'),
]
