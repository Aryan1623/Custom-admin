from django.urls import path
from django.contrib import admin
from . models import Product, UserAttendance

# Register your models here



admin.site.register(Product)
admin.site.register(UserAttendance)



