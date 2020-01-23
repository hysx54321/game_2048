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
            if not follow.active:
                messages.add_message(request, messages.INFO, 'Successfully followed ' + str(user))
                follow.active = True
                follow.updated = timezone.now()
            else:
                messages.add_message(request, messages.WARNING, 'You have already followed ' + str(user))
        else:
            follow = Follow(follower=request.user, user=user)
            messages.add_message(request, messages.INFO, 'Successfully followed ' + str(user))
        follow.save()
    return HttpResponseRedirect(reverse('user-following'))


@login_required
def remove_follow(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('users'))
    user = User.objects.filter(id=request.POST.get('user_id'))
    user = user[0]
    follow = Follow.objects.filter(follower=request.user, user=user)
    follow = follow[0]
    follow.active = False
    follow.updated = timezone.now()
    follow.save()
    messages.add_message(request, messages.INFO, 'Successfully un-followed ' + str(user))
    return HttpResponseRedirect(reverse('user-following'))
