from django.urls import path
from . import views


urlpatterns = [
    path('', views.pepa_main_page, name='pepa_main_page'),
    path('pepa_full_tym', views.full_tym, name= 'pepa_full_tym'),
    path('<int:id>', views.detail_hrace, name='detail_hrace'),
    path('pepa_leaderboard', views.leaderboard, name='pepa_leaderboard'),
    path('pepa_detail_statistika', views.detail_statistika, name='pepa_detail_statistika'),
    path('pepa_jednotlive_dny', views.jednotlive_dny, name='pepa_jednotlive_dny'),
]
