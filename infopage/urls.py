from django.urls import path
from . import views


urlpatterns = [
    path('', views.info, name='home-page'),
    path('all_leaderboard', views.all_leaderboard, name='all_leaderboard'),
]
