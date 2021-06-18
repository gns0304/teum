from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import datetime
import time

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


def logout(request):
    auth.logout(request)
    return redirect('index')

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        return render(request, 'index.html')

@login_required
def dashboard(request):
    user = request.user
    
    favorite_station = FavoriteStation.objects.filter(user = request.user)
    try:
        first_station = Station.objects.filter(name = favorite_station[0].station)
        print(first_station[0].name)
        #코드야 미안해
        find_door = Door.objects.filter(station = first_station.first())
        print(find_door) #해당역의 모든 문
        min_door = find_door.first()
        for f in find_door:
            if f.distance < min_door.distance:
                    min_door = f #최단 이격거리 문
        print(min_door)
        #코드야 미안해2
        date = datetime.date.today()
        dw = date.weekday()
        day = 1 # 평일/토/일
        if dw ==5:
            day = 2
        elif dw == 6:
            day = 3
        find_complexity = Complexity.objects.filter(station = first_station.first(), day = day)
        now = time.localtime() #현재시간
        now_hour = now.tm_hour # 현재 hour
        now_min = now.tm_min # 현재 min
        all_times = Time.objects.filter(complex_id = find_complexity.first()) #해당 역의 모든 시간대 복잡도
        for a in all_times:
            if str(now_hour) == str(a.time)[:2]:
                if str(now_min) > str(a.time)[3:5]:   
                    find_time = a
                    
        try:            
                complexity = find_time.complexity
                if complexity <= 80:
                    find_complexity = "여유"
                elif complexity <= 130:
                    find_complexity = "보통"
                elif complexity <= 150:
                    find_complexity = "주의"
                else:
                    find_complexity = "혼잡"
        except:
                find_complexity="운행종료"
        station_name = first_station[0].name,
        station_line = str(first_station[0].name)+"호선"
        shortest_door = str(min_door.car_number)+'-'+str(min_door.door_number)
    except:
        station_name="즐겨찾는 역을 추가해주세요"
        station_line =""
        shortest_door =""
        find_complexity=""
    

    context = {
            'username': user.username,
            'station_name':station_name,
            'station_line':station_line,
            'shortest_door' : shortest_door,
            'complexity' : find_complexity,
            
        }
    return render(request, "dashboard/dashboard.html",context)

@login_required
def menu(request):
    return render(request, "dashboard/menu.html")

@login_required
def detail(request):
    user = request.user
    favorite_station = FavoriteStation.objects.filter(user = request.user)
    print(favorite_station)
    return render(request, "dashboard/detail.html",{'favorite_station' : favorite_station})

@login_required
def favorite_add(request):
    if request.method == 'POST':
        favorite_stat = FavoriteStation()
        favorite_stat.user = request.user
        favorite_stat.station = request.POST['station']
        favorite_stat.save()
    return render(request,'dashboard/dashboard.html')

@login_required
def favorite_remove(request, station_id):
    station = get_object_or_404(Station, pk=station_id)
    remove_station = FavoriteStation.objects.filter(user = request.user, station = station)
    remove_station.first().delete()
    return render(request,'dashboard/dashboard.html')


def search_shortest(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            line = request.POST['line']
            station = request.POST['station']
            way = request.POST['way']
            find_station = Station.objects.filter(line=line, name = station, platform = way) #찾으려는 역
            print(find_station)
            find_door = Door.objects.filter(station = find_station.first())
            print(find_door) #해당역의 모든 문
            min_door = find_door.first()
            for f in find_door:
                if f.distance < min_door.distance:
                    min_door = f #최단 이격거리 문

            context = {
                #임시이름
                'station_title' : find_station[0],
                'platform_title' : find_station[0].platform,
                'big_car_door_title' : str(min_door.car_number)+'-'+str(min_door.door_number),
                'distanceInfo_titles' : min_door.distance,
            }

            print(context["big_car_door_title"])

            return render(request,"results/shortestDistance.html",context)
    return render(request, "search/shortestDistance.html")


def search_door(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            line = request.POST['line']
            station = request.POST['station']
            way = request.POST['way']
            car_number = request.POST['car_number']
            door_number = request.POST['door_number']
            find_station = Station.objects.filter(line=line, name = station, platform = way)
            find_door = Door.objects.filter(station = find_station.first(), car_number = car_number, door_number = door_number)
            
            #코드야 미안해
            date = datetime.date.today()
            dw = date.weekday()
            day = 1 # 평일/토/일
            if dw ==5:
                day = 2
            elif dw == 6:
                day = 3
            find_complexity = Complexity.objects.filter(station = find_station.first(), day = day)
            now = time.localtime() #현재시간
            now_hour = now.tm_hour # 현재 hour
            now_min = now.tm_min # 현재 min
            all_times = Time.objects.filter(complex_id = find_complexity.first()) #해당 역의 모든 시간대 복잡도
            for a in all_times:
                if str(now_hour) == str(a.time)[:2]:
                    if str(now_min) > str(a.time)[3:5]:   
                        find_time = a
            try:            
                complexity = find_time.complexity
                if complexity <= 80:
                    find_complexity = "여유"
                elif complexity <= 130:
                    find_complexity = "보통"
                elif complexity <= 150:
                    find_complexity = "주의"
                else:
                    find_complexity = "혼잡"
            except:
                find_complexity="운행종료"


            context = {
                #임시이름
                'station_title' : find_station[0],
                'platform_title' : find_station[0].platform,
                'car_door_title' : str(find_door[0].car_number)+'-'+str(find_door[0].door_number)+" 출입문",
                'distance_title' : find_door[0].distance,
                'flowInfo_title' : find_complexity,
            }

            print(context)

            return render(request,"results/doorDistance.html",context)

    return render(request, "search/doorDistance.html")


def search_complexity(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            line = request.POST['line']
            station = request.POST['station']
            way = request.POST['way']
            find_station = Station.objects.filter(line=line, name = station, platform = way)
            date = datetime.date.today()
            dw = date.weekday()
            day = 1 # 평일/토/일
            if dw ==5:
                day = 2
            elif dw == 6:
                day = 3
            find_complexity = Complexity.objects.filter(station = find_station.first(), day = day)
            print(find_complexity)
            
            now = time.localtime() #현재시간
            now_hour = now.tm_hour # 현재 hour
            now_min = now.tm_min # 현재 min
            all_times = Time.objects.filter(complex_id = find_complexity.first()) #해당 역의 모든 시간대 복잡도
            for a in all_times:
                if str(now_hour) == str(a.time)[:2]:
                    if str(now_min) > str(a.time)[3:5]:   
                        find_time = a
                        
            try:            
                complexity = find_time.complexity
                if complexity <= 80:
                    find_complexity = "여유"
                elif complexity <= 130:
                    find_complexity = "보통"
                elif complexity <= 150:
                    find_complexity = "주의"
                else:
                    find_complexity = "혼잡"
            except:
                find_complexity="운행종료"
            context = {
                #임시이름
                'station_title' : find_station[0],
                'platform_title' : find_station[0].platform,
                'flowInfo_title' : find_complexity,
            }

            print(context)

            return render(request,"results/complexity.html",context)
    return render(request, "search/complexity.html")

#얘네 왜 있냐?
def detail_shortest(request,door_id):

    
    return render(request, "results/shortestDistance.html")


def detail_door(request,door_id):
    return render(request, "results/doorDistance.html")


def detail_complexity(request,time_id):
    return render(request, "results/complexity.html")


def test_complexity(request):
    return render(request, "results/complexity.html")

def test_shortest(request):
    return render(request, "results/shortest.html")

def test_door(request):
    return render(request, "results/door.html")


# for Ajax

import json
from django.http import HttpResponse


def get_station_data(request):
    line_number = request.GET["line"]

    if line_number != 0:
        stations = Station.objects.filter(line=line_number)
        station_list = []

        for station in stations:
            station_list.append(station.name)

        context = {"station": list(set(station_list))}

    return HttpResponse(json.dumps(context), content_type="application/json")


def get_platform_data(request):
    station_name = request.GET["station"]

    print(station_name)

    if station_name != "역명 선택":
        stations = Station.objects.filter(name=station_name)

        platforms = []

        for station in stations:
            platforms.append(station.platform)

        context = {"platforms": list(set(platforms))}

        print(context)

    return HttpResponse(json.dumps(context), content_type="application/json")


