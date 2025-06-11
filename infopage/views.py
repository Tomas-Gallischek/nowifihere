from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import vysledky_hracu

hraci = vysledky_hracu.objects.all()


def info(request):
    return render(request, 'infopage/index.html')


def all_leaderboard(request):
    return render(request, 'infopage/leaderboard_all.html', {
        'vsichni_hraci': hraci,
    })