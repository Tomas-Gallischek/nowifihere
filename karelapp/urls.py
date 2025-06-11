from django.urls import path
from . import views

urlpatterns = [
    path('', views.karel_main_page),
]
