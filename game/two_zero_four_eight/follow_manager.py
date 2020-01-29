from django.utils import timezone


def save(follow):
    follow.active = True
    follow.updated = timezone.now()
    follow.user.num_follower += 1
    follow.follower.num_following += 1
    follow.user.save()
    follow.follower.save()
    follow.save()


def remove(follow):
    follow.active = False
    follow.updated = timezone.now()
    follow.user.num_follower -= 1
    follow.follower.num_following -= 1
    follow.user.save()
    follow.follower.save()
    follow.save()
