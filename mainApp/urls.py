from django.urls import path, include
from mainApp import views

urlpatterns = [

    path('', views.index, name="index"),
    path('logout', views.logout, name="logout"),

    # 대시보드 관련

    path('dashboard', views.dashboard, name="dashboard"),
    path('dashboard/menu', views.menu, name="menu"),
    path('dashboard/detail', views.detail, name="detail"),

    # 즐겨 찾기 기능

    path('dashboard/favorite/add/<int:station_id>', views.favorite_add, name="favorite_add"),
    path('dashboard/favorite/remove/<int:station_id>', views.favorite_remove, name="favorite_remove"),

    # 검색 관련

    path('detail/shortest/', views.search_shortest, name="search_shortest"),
    path('detail/door', views.search_door, name="search_door"),
    path('detail/complexity', views.search_complexity, name="search_complexity"),

    # 결과 화면 (렌더 논의에 따라 사용되지 않을 수 있음)
    #
    path('result/shortest/<int:door_id>', views.detail_shortest, name="detail_shortest"),
    path('result/door/<int:door_id>', views.detail_door, name="detail_door"),
    path('result/complexity/<int:time_id>', views.detail_complexity, name="detail_complexity"),

    # 테스트용

    path('test/shortest', views.test_shortest, name="test_shortest"),
    path('test/door', views.test_door, name="test_door"),
    path('test/complexity', views.test_complexity, name="test_complexity"),


    #for ajax

    path('get/station', views.get_station_data, name="get_station_data"),
    path('get/platform', views.get_platform_data, name="get_platform_data"),


]