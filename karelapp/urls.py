from django.urls import path
from . import views


urlpatterns = [
    path('', views.karel_main_page, name='karel_main_page'),
    path('karel_full_tym', views.full_tym, name= 'karel_full_tym'),
    path('<int:id>', views.detail_hrace, name='karel_detail_hrace'),
    path('karel_leaderboard', views.leaderboard, name='karel_leaderboard'),
    path('karel_detail_statistika', views.detail_statistika, name='karel_detail_statistika'),
    path('karel_jednotlive_dny', views.jednotlive_dny, name='karel_jednotlive_dny'),
]
