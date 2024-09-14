from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard', views.dash, name='dashboard'),
    path('user-list/', views.user_list_view, name='user_list'),
    path('<str:username>/attendance/', views.attendance, name='user_attendance'),
]