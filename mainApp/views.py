from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

# for allauth


def get_username(request):

    user = get_object_or_404(User, username=request.user)
    user_name = user.get_full_name()
    social_user = get_object_or_404(SocialAccount, user=request.user)

    if user_name == "" or user_name != social_user.extra_data["name"]:

        user.last_name = social_user.extra_data["name"][:1]
        user.first_name = social_user.extra_data["name"][1:]
        user.save()

    return user.last_name + user.first_name

# Create your views here.


def index(request):

    return render(request, 'index.html')


def dashboard(request):
    return render(request, "dashboard/dashboard.html")


def menu(request):
    return render(request, "dashboard/menu.html")


def detail(request):
    return render(request, "dashboard/detail.html")


def favorite_add(request, station_id):
    pass


def favorite_remove(request, station_id):
    pass


def search_shortest(request):
    pass


def search_door(request):
    pass


def search_complexity(request):
    pass


def detail_shortest(request):
    pass


def detail_door(request):
    pass


def detail_complexity(request):
    pass



