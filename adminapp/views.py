from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from pepaapp.views import pepa_energie_procenta, pepa_kondice_procenta, pepa_sytost_procenta, pepa_hydratace_procenta, pepa_zatez_procenta, pepa_volna_kapacita_procenta, PEPA_FINAL_KM, pepa_xp, pepa_celkova_vaha
from karelapp.views import karel_energie_procenta, karel_kondice_procenta, karel_sytost_procenta, karel_hydratace_procenta, karel_zatez_procenta, karel_volna_kapacita_procenta, KAREL_FINAL_KM, karel_xp, karel_celkova_vaha
from brunhildaapp.views import brunhilda_energie_procenta, brunhilda_kondice_procenta, brunhilda_sytost_procenta, brunhilda_hydratace_procenta, brunhilda_zatez_procenta, brunhilda_volna_kapacita_procenta, BRUNHILDA_FINAL_KM, brunhilda_xp, brunhilda_celkova_vaha


from infopage.models import vysledky_hracu


vsichni_hraci = vysledky_hracu.objects.all()
hraci_pepa = vysledky_hracu.objects.filter(tym="pepa")
hraci_karel = vysledky_hracu.objects.filter(tym="karel")
hraci_brunhilda = vysledky_hracu.objects.filter(tym="brunhilda")


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
        'pepa_vaha': pepa_celkova_vaha,
        'karel_energie': karel_energie_procenta,
        'karel_kondice': karel_kondice_procenta,
        'karel_sytost': karel_sytost_procenta,
        'karel_hydratace': karel_hydratace_procenta,
        'karel_zatez': karel_zatez_procenta, 
        'karel_volna_kapacita': karel_volna_kapacita_procenta,
        'karel_km': KAREL_FINAL_KM,
        'karel_xp': karel_xp,
        'karel_vaha': karel_celkova_vaha,
        'brunhilda_energie': brunhilda_energie_procenta,
        'brunhilda_kondice': brunhilda_kondice_procenta,
        'brunhilda_sytost': brunhilda_sytost_procenta,
        'brunhilda_hydratace': brunhilda_hydratace_procenta,
        'brunhilda_zatez': brunhilda_zatez_procenta, 
        'brunhilda_volna_kapacita': brunhilda_volna_kapacita_procenta,
        'brunhilda_km': BRUNHILDA_FINAL_KM,
        'brunhilda_xp': brunhilda_xp,
        'brunhilda_vaha': brunhilda_celkova_vaha
            })

def adminpage(request):
    return render(request, 'adminapp/main_admin_page.html')

def detail_vsech_hracu(request):
    return render(request, 'adminapp/detail_vsech_hracu.html', {
        "vsichni_hraci": vsichni_hraci,
        "hraci_pepa": hraci_pepa,
        'hraci_karel': hraci_karel,
        'hraci_brunhilda': hraci_brunhilda
    })
