from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='chartapp/login.html'), name='login'),
    path('logout', views.custom_logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('accounts/profile/attendance', views.attendance_list, name='attendance_list'),
    path('accounts/profile/',views.index , name='index2')
    
]
