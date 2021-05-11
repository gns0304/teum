from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

# for allauth

def getUsername(request):

    user = get_object_or_404(User, username=request.user)
    userName = user.get_full_name()
    socialUser = get_object_or_404(SocialAccount, user=request.user)

    if userName == "" or userName != socialUser.extra_data["name"]:

        user.last_name = socialUser.extra_data["name"][:1]
        user.first_name = socialUser.extra_data["name"][1:]
        user.save()

    return user.last_name + user.first_name

# Create your views here.

def index(request):

    print(getUsername(request))
    return render(request, 'index.html')

