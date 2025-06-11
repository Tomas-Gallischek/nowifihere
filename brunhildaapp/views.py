from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

def brunhilda_main_page(request):
    return render(request, 'brunhildaapp/brunhilda_main_page.html')