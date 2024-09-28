from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_co2_consumption/', views.add_co2_consumption, name='add_co2_consumption'),
    path('view_co2_consumption/', views.view_co2_consumption, name='view_co2_consumption'),
]