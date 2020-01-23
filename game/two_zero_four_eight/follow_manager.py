from django.utils import timezone

from two_zero_four_eight.models import User, Game, Follow
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def add_follow(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('users'))
    user = User.objects.filter(id=request.POST.get('user_id'))
    user = user[0]
    existing_follow = Follow.objects.filter(follower=request.user, user=user)
    if request.user == user:
        messages.add_message(request, messages.ERROR, 'You cannot follow yourself!')
    else:
        if existing_follow:
            follow = existing_follow[0]
            if follow.active:
                messages.add_message(request, messages.WARNING, 'You have already followed ' + str(user))
                return HttpResponseRedirect(reverse('user-following'))
            else:
                follow.active = True
                follow.updated = timezone.now()
        else:
            follow = Follow(follower=request.user, user=user)
        messages.add_message(request, messages.INFO, 'Successfully followed ' + str(user))
        follow.save()
        request.user.num_following += 1
        request.user.save()
        user.num_follower += 1
        user.save()
    return HttpResponseRedirect(reverse('user-following'))


@login_required
def remove_follow(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('users'))
    user = User.objects.filter(id=request.POST.get('user_id'))
    user = user[0]
    follow = Follow.objects.filter(follower=request.user, user=user)
    follow = follow[0]

    # TODO: when follow doesn't exist or is not active, do something

    follow.active = False
    follow.updated = timezone.now()
    follow.save()
    request.user.num_following -= 1
    request.user.save()
    user.num_follower -= 1
    user.save()
    messages.add_message(request, messages.INFO, 'Successfully un-followed ' + str(user))
    return HttpResponseRedirect(reverse('user-following'))
