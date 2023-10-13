
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('secured_hello/', views.secured_hello),
    path('unsecured_hello/', views.unsecured_hello),
    path('login/', views.login),
    path('logout/', views.logout),
    path('refresh-token/', views.refresh_token),
    path('create-user/',views.create_user),
    path('change-password/',views.change_password),
    path('get-users/', views.get_users)
]