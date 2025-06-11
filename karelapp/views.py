from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


def karel_main_page(request):
    return render(request, 'karelapp/karel_main_page.html')