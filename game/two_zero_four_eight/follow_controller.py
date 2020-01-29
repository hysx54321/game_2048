from django.utils import timezone

from two_zero_four_eight.follow_manager import save, remove
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
    user = get_object_or_404(User, id=request.POST.get('user_id'))
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
            follow = Follow(follower=request.user, user=user)
        save(follow)
        messages.add_message(request, messages.INFO, 'Successfully followed ' + str(user))
    return HttpResponseRedirect(reverse('user-following'))


@login_required
def remove_follow(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('users'))
    user = get_object_or_404(User, id=request.POST.get('user_id'))
    follow = get_object_or_404(Follow, follower=request.user, user=user)
    # follow = Follow.objects.filter(follower=request.user, user=user)
    # follow = follow[0]

    # TODO: when follow doesn't exist or is not active, do something

    remove(follow)
    messages.add_message(request, messages.INFO, 'Successfully un-followed ' + str(user))
    return HttpResponseRedirect(reverse('user-following'))


@login_required
def remove_follower(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('users'))
    user = get_object_or_404(User, id=request.POST.get('user_id'))
    follow = get_object_or_404(Follow, follower=user, user=request.user)
    # follow = Follow.objects.filter(follower=request.user, user=user)
    # follow = follow[0]

    # TODO: when follow doesn't exist or is not active, do something

    remove(follow)
    messages.add_message(request, messages.INFO, 'Successfully removed the follower ' + str(user))
    return HttpResponseRedirect(reverse('user-follower'))
