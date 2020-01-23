from django.contrib import admin

# Register your models here.
from .models import Game, Follow, User

admin.site.register(Game)
admin.site.register(Follow)
admin.site.register(User)
