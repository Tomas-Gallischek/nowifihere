from django.urls import path
from . import views


urlpatterns = [
    path('', views.brunhilda_main_page, name='brunhilda_main_page'),
    path('brunhilda_full_tym', views.full_tym, name= 'brunhilda_full_tym'),
    path('<int:id>', views.detail_hrace, name='brunhilda_detail_hrace'),
    path('brunhilda_leaderboard', views.leaderboard, name='brunhilda_leaderboard'),
    path('brunhilda_detail_statistika', views.detail_statistika, name='brunhilda_detail_statistika'),
    path('brunhilda_jednotlive_dny', views.jednotlive_dny, name='brunhilda_jednotlive_dny'),
]
