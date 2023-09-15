
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('hello/', views.get_auth),
    path('secured_hello/', views.secured_hello)
]