from django.db.models import Max
from django.utils import timezone

from django.db import models

# Create your models here.
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from two_zero_four_eight.fields.GameReconstructionField import *


def binary_search(array, number):
    hi = len(array)
    lo = 0
    while hi > lo:
        mid = lo + int((hi - lo + 1) / 2)
        # print(mid, hi, lo)
        if array[mid] <= number:
            lo = mid
        else:
            hi = mid - 1
    return lo


experience_table = [0, 800, 2000, 3500, 5500, 7900, 10900, 14200, 17800, 21700, 25900, 30400, 35200, 40300, 45700,
                    51400, 57400,
                    63700,
                    70300, 84400, 91900, 107800, 116200, 124900, 133900, 143200, 152800, 162700, 172900, 183400, 194200,
                    205300,
                    216700, 228400, 240400, 252700, 265300, 278200, 291400, 304900, 318300, 332800, 361900, 376900,
                    392200,
                    407800, 423700, 439900, 100000000000]

vip_table = [0, 100, 500, 1200, 2000, 5000, 15000, 25000, 50000, 10000000000]


def status_string(level, experience, table):
    return str(level) + ' (' + str(experience - table[level]) + ' / ' + str(table[level + 1] - table[level]) + ')'


class User(AbstractUser):
    # game_played = models.IntegerField(verbose_name='Number of Games Played', default=0)
    # best_game = models.ForeignKey()
    # highest_score = models.PositiveIntegerField(verbose_name='Highest Score', null=True, blank=True)
    # fastest_solve = models.PositiveIntegerField(verbose_name='Fastest Solve', null=True, blank=True)
    experience = models.IntegerField(verbose_name='Experience', default=0)
    money_deposited = models.IntegerField(verbose_name='Money Deposited', default=0)

    # num_follower = models.IntegerField(verbose_name='Followers', default=0)
    # num_following = models.IntegerField(verbose_name='Followings', default=0)

    # Metadata
    class Meta:
        ordering = ['date_joined']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('user-detail', args=[str(self.id)])

    @property
    def level(self):
        return binary_search(number=self.experience, array=experience_table)

    @property
    def level_string(self):
        return 'Level ' + status_string(level=self.level, experience=self.experience, table=experience_table)

    @property
    def vip_level(self):
        return binary_search(number=self.money_deposited, array=vip_table)

    @property
    def vip_level_string(self):
        return 'VIP ' + status_string(level=self.vip_level, experience=self.money_deposited, table=vip_table)

    @property
    def num_follower(self):
        return Follow.objects.filter(user=self).count

    @property
    def num_following(self):
        return Follow.objects.filter(follower=self).count

    @property
    def game_played(self):
        return Game.objects.filter(player=self).count

    @property
    def highest_score(self):
        result = Game.objects.filter(player=self).aggregate(max_score=Max('score'))
        return result.get('max_score')


class Game(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    score = models.PositiveIntegerField(verbose_name='Score')
    started_at = models.DateTimeField(default=timezone.now)
    duration_second = models.PositiveIntegerField(verbose_name='Duration in Second')
    time_2048_second = models.PositiveIntegerField(verbose_name='Time taken to achieve 2048', null=True, blank=True)
    move = models.PositiveIntegerField(verbose_name='Number of Moves', default=0)
    useless_move = models.IntegerField(verbose_name='Number of useless moves', default=0)
    game_reconstruction = models.TextField(verbose_name='Game Reconstruction', null=True, default=None)

    # Metadata
    class Meta:
        ordering = ['-started_at']
        index_together =['player', 'score']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('game-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return 'player: ' + str(self.player) + ' score: ' + str(self.score) + ' time: ' + str(self.started_at)


class Follow(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='follower')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    # Metadata
    class Meta:
        ordering = ['user']
        unique_together = ('user', 'follower',)
        index_together = ["user", "follower"]

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return str(self.user) + ' is followed by ' + str(self.follower)

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.user == self.follower:
            raise ValidationError(_('The follower and the user cannot be the same.'))
