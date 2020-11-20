from django.urls import path
from . import views

urlpatterns = [
    path('register', views.userCreate),
    path('login', views.userLogin),
]
