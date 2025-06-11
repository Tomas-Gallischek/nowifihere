from django.urls import path
from . import views


urlpatterns = [
    path('', views.adminpage, name='adminpage'),
    path('statistiky_avataru', views.statistiky),
    path('detail_hracu', views.detail_vsech_hracu),
]
