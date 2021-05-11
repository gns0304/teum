from django.urls import path, include
from mainApp import views

urlpatterns = [

    path('', views.index, name="index"),

]