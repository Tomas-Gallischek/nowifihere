from django.urls import path
from . import views


urlpatterns = [
    path('', views.brunhilda_main_page),
]
