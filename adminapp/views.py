from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from pepaapp.views import pepa_energie_procenta, pepa_kondice_procenta, pepa_sytost_procenta, pepa_hydratace_procenta, pepa_zatez_procenta, pepa_volna_kapacita_procenta, PEPA_FINAL_KM, pepa_xp, pepa_celkova_vaha
from infopage.models import vysledky_hracu


vsichni_hraci = vysledky_hracu.objects.all()


def statistiky(request):
    return render(request, 'adminapp/statistiky_avataru.html', {
        'pepa_energie': pepa_energie_procenta,
        'pepa_kondice': pepa_kondice_procenta,
        'pepa_sytost': pepa_sytost_procenta,
        'pepa_hydratace': pepa_hydratace_procenta,
        'pepa_zatez': pepa_zatez_procenta, 
        'pepa_volna_kapacita': pepa_volna_kapacita_procenta,
        'pepa_km': PEPA_FINAL_KM,
        'pepa_xp': pepa_xp,
        'pepa_vaha': pepa_celkova_vaha

            })

def adminpage(request):
    return render(request, 'adminapp/main_admin_page.html')

def detail_vsech_hracu(request):
    return render(request, 'adminapp/detail_vsech_hracu.html', {
        "vsichni_hraci": vsichni_hraci
    })