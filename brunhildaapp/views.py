# IMPORT - FUNKCE:
from multiprocessing import context
from re import A
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Sum
from django.db.models import Avg, Sum
import os
import random

# IMPORT - MODELY:
from adminapp.models import aktualniden, food_drink, vybava, aktivita_kcal2, kondice_hubnuti, spanek, hraci_v_tymu, pamet_brunhilda, motivacni_citat
from .models import brunhilda_zakladni_staty, brunhilda_snedl, brunhilda_snedl_polozka, brunhilda_equip, InventarPolozkaFood, InventarPolozkaVybava, brunhilda_inv
from infopage.models import vysledky_hracu

# POČET HRÁČŮ V TÝMECH
pocet_hracu_pepa_objekt = hraci_v_tymu.objects.get(id=1)
pocet_hracu_pepa = pocet_hracu_pepa_objekt.pocet_hracu_pepa

pocet_hracu_karel_objekt = hraci_v_tymu.objects.get(id=1)
pocet_hracu_karel = pocet_hracu_karel_objekt.pocet_hracu_karel

pocet_hracu_brunhilda_objekt = hraci_v_tymu.objects.get(id=1)
pocet_hracu_brunhilda = pocet_hracu_brunhilda_objekt.pocet_hracu_brunhilda

pocet_hracu_celkem = (pocet_hracu_pepa)+(pocet_hracu_karel)+(pocet_hracu_brunhilda)

# ZÁKLADNÍ STATY
zakladni_staty = brunhilda_zakladni_staty.objects.get(id=1)

# AKTUÁLNÍ DEN
aktualni_den_objekt = aktualniden.objects.get(id=1)
aktualni_den = aktualni_den_objekt.cislo_dne
nasledujici_den = aktualni_den+1

# BRUNHILDIN AKTUÁLNÍ EQUIP
aktual_equip = brunhilda_equip.objects.get(den=aktualni_den)
aktual_equip_boty_nazev = aktual_equip.equip_boty
aktual_equip_ponozky_nazev = aktual_equip.equip_ponozky
aktual_equip_kalhoty_nazev = aktual_equip.equip_kalhoty
aktual_equip_triko_nazev = aktual_equip.equip_triko
aktual_equip_doplnek_nazev = aktual_equip.equip_doplnek 
aktual_equip_batoh_nazev = aktual_equip.equip_batoh
aktual_equip_spacak_nazev = aktual_equip.equip_spacak
aktual_equip_karimatka_nazev = aktual_equip.equip_karimatka

# EQUIP - BONUSY
BONUS_delka_kroku_procenta = aktual_equip.equip_BONUS_delka_kroku_procenta+1
BONUS_BMR_procenta = aktual_equip.equip_BONUS_BMR_procenta
BONUS_zatez_procenta = aktual_equip.equip_BONUS_zatez_procenta
BONUS_income_flat = aktual_equip.equip_BONUS_income_flat
BONUS_income_procenta = aktual_equip.equip_BONUS_income_procenta+1
BONUS_kapacita_flet = aktual_equip.equip_BONUS_kapacita_flet
BONUS_kapacita_procenta = aktual_equip.equip_BONUS_kapacita_procenta+1
BONUS_XP_flat =aktual_equip.equip_BONUS_XP_flat
BONUS_XP_procenta =aktual_equip.equip_BONUS_XP_procenta+1
BONUS_spanek_flat =aktual_equip.equip_BONUS_spanek_flat
BONUS_spanek_procenta =aktual_equip.equip_BONUS_spanek_procenta+1
BONUS_cena_procenta =aktual_equip.equip_BONUS_cena_procenta+1


boty_img = os.path.join("images","vybava","boty", f"{aktual_equip_boty_nazev}.png")
ponozky_img = os.path.join("images","vybava","Ponožky", f"{aktual_equip_ponozky_nazev}.png")
kalhoty_img = os.path.join("images","vybava","Kalhoty", f"{aktual_equip_kalhoty_nazev}.png")
triko_img = os.path.join("images","vybava","Trička", f"{aktual_equip_triko_nazev}.png")
doplnek_img = os.path.join("images","vybava","Doplňky", f"{aktual_equip_doplnek_nazev}.png")
batoh_img = os.path.join("images","vybava","Batohy", f"{aktual_equip_batoh_nazev}.png")
spacak_img = os.path.join("images","vybava","Spacáky", f"{aktual_equip_spacak_nazev}.png")
karimatka_img = os.path.join("images","vybava","KARIMATKA", f"{aktual_equip_karimatka_nazev}.png")

# VČEREJŠÍ DEN < --- Kvůli paměti
vcerejsi_den = (aktualni_den)-(1)
pamet_vcera = pamet_brunhilda.objects.get(den=vcerejsi_den)
energie_vcera = pamet_vcera.energie
kondice_vcera = pamet_vcera.kondice
hydratace_vcera = pamet_vcera.hydratace
sytost_vcera = pamet_vcera.sytost
zatez_vcera = pamet_vcera.zatez
volna_kapacita_vcera = pamet_vcera.volna_kapacita
brunhildina_aktualni_vaha_vcera = pamet_vcera.brunhilda_aktualni_vaha # Zde ponecháno pepova_... dle původního modelu pamet_

# BMI
brunhilda_BMI = (((zakladni_staty.vaha)/((zakladni_staty.vyska)/100)**2))
brunhilda_BMI = round(brunhilda_BMI,2)

# BMR - 10*VÁHA, + 6,25*VÝŠKA - 5*VĚK +5
brunhilda_BMR = (((zakladni_staty.vaha)*10) + ((zakladni_staty.vyska)*6.25) - ((zakladni_staty.vek)*5) +5)
brunhilda_BMR = (brunhilda_BMR)+((brunhilda_BMR)*(BONUS_BMR_procenta)) #<--- Jelikož v závorce je - tak před ní musí být +
brunhilda_BMR = round(brunhilda_BMR,2)


# DENNÍ PRŮMĚR KROKŮ - DNES
dnesni_prumer_kroku=1

if aktualni_den > 1 and aktualni_den <= 12:
    sloupec = f'kroky{aktualni_den}'
    dnesni_prumer_kroku = vysledky_hracu.objects.filter(tym="brunhilda").aggregate(Avg(sloupec))[f'{sloupec}__avg']
else:
    brunhilda_kroky_bonus = vysledky_hracu.objects.filter(tym="brunhilda")
    for hrac in brunhilda_kroky_bonus:
        dnesni_prumer_kroku += hrac.kroky_BONUS
    dnesni_prumer_kroku = (round((dnesni_prumer_kroku)/(pocet_hracu_brunhilda)))

# SOUČET KROKŮ ZA JEDNOTLIVÉ DNY CELÝ TÝM
agregovane_hodnoty = vysledky_hracu.objects.filter(tym="brunhilda").aggregate(
    sum_kroky_bonus=Sum('kroky_BONUS'),
    sum_kroky1=Sum('kroky1'),
    sum_kroky2=Sum('kroky2'),
    sum_kroky3=Sum('kroky3'),
    sum_kroky4=Sum('kroky4'),
    sum_kroky5=Sum('kroky5'),
    sum_kroky6=Sum('kroky6'),
    sum_kroky7=Sum('kroky7'),
    sum_kroky8=Sum('kroky8'),
    sum_kroky9=Sum('kroky9'),
    sum_kroky10=Sum('kroky10'),
    sum_kroky11=Sum('kroky11'),
    sum_kroky12=Sum('kroky12'),
)
suma_kroky = sum(agregovane_hodnoty.values())

# CELKOVÝ POČET KROKŮ - JEDNOTLIVÍ HRÁČI
hraci = vysledky_hracu.objects.filter(tym="brunhilda")
for hrac in hraci:
    hrac.celkem_kroku = (
        hrac.celkem_kroku
    )

# KOLIK KM ZA DEN BRUNHILDA UŠLA <--- Bez bonusů, je potřeba na výpočty
delka_kroku = (zakladni_staty.delkakroku)*(BONUS_delka_kroku_procenta)
brunhilda_km_dnes = round((((dnesni_prumer_kroku)*(delka_kroku)/100)/1000), 2)

# KAPACITA
# brunhildin aktualni batoh
if BONUS_kapacita_flet == 0:
    BONUS_kapacita_flet = 5
kapacita_batohu = (BONUS_kapacita_flet)*(BONUS_kapacita_procenta)

# objem inventáře (všechno co brunhilda má)
brunhilda_inv_instance = brunhilda_inv.objects.get(den=aktualni_den)  # Získání objektu s daným dnem
objem_inv = round(brunhilda_inv_instance.objem_inventare,2)  # Získání hodnoty equip_objem

# objem toho co má brunhilda na sobě (protože to nezabírá místo v batohu)
brunhilda_equip_objem = brunhilda_equip.objects.get(den=aktualni_den)
brunhilda_equip_objem = brunhilda_equip_objem.equip_objem

# brunhildina volná kapacita
volna_kapacita = round((((kapacita_batohu)-(objem_inv))),2)
volna_kapacita_procenta = round((volna_kapacita)/((kapacita_batohu)/100))


if volna_kapacita<0:
    volna_kapacita_procenta=0.1
if volna_kapacita>150:
    volna_kapacita_procenta=150

# TEMPO
aktivita_dnes = spanek.objects.get(den=(aktualni_den))
tempo = round(((brunhilda_km_dnes)/(aktivita_dnes.brunhilda_aktivita)),1)
if tempo == 0:
    tempo = 3


# SUMA KONZUMACE - KALORIE + SYTOST + HYDRATACE + HMOTNOST

# KALORIE <--- příjem
sum_kcal_dnes = brunhilda_snedl.objects.get(den=aktualni_den)
sum_kcal_dnes = sum_kcal_dnes.snedeno_kcal

# HYDRATACE
hydratace_jidlo = 1
dnesni_zaznam_hydratace = brunhilda_snedl.objects.get(den=aktualni_den)
hydratace_jidlo = dnesni_zaznam_hydratace.snedeno_hydratace
hydratace = ((hydratace_vcera)-(65)+hydratace_jidlo)
hydratace_procenta = round(hydratace)

if hydratace<0.1:
    hydratace_procenta=0.1
if hydratace>150:
    hydratace_procenta=150

if hydratace_procenta >= 120:
    negace_energie_hydratace = 0.55
elif hydratace_procenta > 100:
    negace_energie_hydratace = 0.75
elif hydratace_procenta < 40:
    negace_energie_hydratace=0.75
elif hydratace_procenta <=20:
    negace_energie_hydratace=0.65
elif hydratace_procenta <5:
    negace_energie_hydratace=0.55
else:
    negace_energie_hydratace=1

#SYTOST
sytost_jidlo = 0
dnesni_zaznam_sytost = brunhilda_snedl.objects.get(den=aktualni_den)
sytost_jidlo = dnesni_zaznam_sytost.snedeno_sytost
sytost = ((sytost_vcera)-(60)+sytost_jidlo)
sytost_procenta = int(round(sytost))


if sytost<0.1:
    sytost_procenta=0.1
if sytost>150:
    sytost_procenta=150

if sytost_procenta > 120:
    negace_energie_sytost = 0.65
elif sytost_procenta > 100:
    negace_energie_sytost = 0.85
elif sytost_procenta < 30:
    negace_energie_sytost=0.85
elif sytost_procenta <15:
    negace_energie_sytost=0.75
else:
    negace_energie_sytost=1

# VÁHA SNĚDENÉHO JÍDLA:
sum_snezene_hmotnost_dnes = brunhilda_snedl.objects.get(den=aktualni_den)
sum_snezene_hmotnost_dnes = sum_snezene_hmotnost_dnes.snedeno_hmotnost

# kcal PŘÍJEM (Jídlo + pití)
kcal_prijem_dnes = sum_kcal_dnes

# kcal VÝDEJ (Bazál + aktivita)
kcal_vydej = aktivita_kcal2.objects.get(tempo=tempo) # <-- Zjištěno kcal/h na základě tempa
doba_aktivity = spanek.objects.get(den=aktualni_den) # <-- zjištěn aktuální den v databázi aktivity
doba_aktivity_dnes = doba_aktivity.brunhilda_aktivita # <-- Zjištěno, kolik hodin byla brunhilda aktivní
kcal_vydej_dnes = ((kcal_vydej.kcal_za_hodinu)*1.5)*(doba_aktivity_dnes) # <-- kolik kalorií brunhilda dneska spálila aktivitou 

kcal_vydej_dnes_SUMA = round(kcal_vydej_dnes)+(brunhilda_BMR) # <-- CELKOVÉ SPLÁLENÉ KALORIE VČETNĚ BAZÁLU

# kcal ROZDÍL (Příjem - výdej)
kcal_rozdil_dnes=round((kcal_prijem_dnes)-(kcal_vydej_dnes_SUMA))

# nabírání/hudnutí - Na základě výpočtu
hubnuti_nabirani = round((((kcal_rozdil_dnes)*(0.3)/1000)),2) # <--- 0.3 je počet GRAMŮ které člověk zhubne za 1 kcal (nasledně převedeno na kg)
kolik_zhubnul_dnes = round(hubnuti_nabirani,2)
# CELKOVÁ VÁHA + PŘIDAVNÁ VÁHA: (přídavná váha ovlivňuje nosnost) 
brunhilda_celkova_vaha = round((brunhildina_aktualni_vaha_vcera) + (kolik_zhubnul_dnes),2)


# NEGACE ENERGIE V PŘÍPADĚ HLADOVĚNÍ
if kcal_rozdil_dnes<-800:
    negace_hubnuti_procenta =85
elif kcal_rozdil_dnes<-600:
    negace_hubnuti_procenta =95
elif kcal_rozdil_dnes<-400:
    negace_hubnuti_procenta =105
elif kcal_rozdil_dnes<-200:
    negace_hubnuti_procenta =110
elif kcal_rozdil_dnes<-100:
    negace_hubnuti_procenta =115
elif kcal_rozdil_dnes<-50:
    negace_hubnuti_procenta =120
elif kcal_rozdil_dnes<50:
    negace_hubnuti_procenta =120
elif kcal_rozdil_dnes<100:
    negace_hubnuti_procenta =115
elif kcal_rozdil_dnes<200:
    negace_hubnuti_procenta =110
elif kcal_rozdil_dnes<400:
    negace_hubnuti_procenta =105
elif kcal_rozdil_dnes<600:
    negace_hubnuti_procenta =100
if kcal_rozdil_dnes<800:
    negace_hubnuti_procenta =95
elif kcal_rozdil_dnes>800:
    negace_hubnuti_procenta =85

# ZÁTĚŽ
nosnost = (brunhilda_celkova_vaha) / 5
brunhilda_inv_instance = brunhilda_inv.objects.get(den=aktualni_den)
zatez = round(((brunhilda_inv_instance.vaha_inventare)+(brunhilda_inv_instance.vaha_inventare*BONUS_zatez_procenta)),2)
zatez_procenta = round(((zatez)/(nosnost/100)))

if zatez<0.1:
    zatez_procenta=0.1
if zatez>150:
    zatez_procenta=150


# SPÁNEK + AKTIVITA <--- Je nutné počítat se včerejším dnem! Do databáze zadávám den zápisu, ale projevuje se to až ten další
spanek_vcera = spanek.objects.get(den=vcerejsi_den)
brunhilda_spanek = ((spanek_vcera.brunhilda_spanek)+(BONUS_spanek_flat))*BONUS_spanek_procenta

if brunhilda_spanek ==0:
    brunhilda_spanek=8

brunhilda_aktivita = spanek_vcera.brunhilda_aktivita

if brunhilda_aktivita == 0:
    brunhilda_aktivita=6

# ENERGIE
energie_bonus_jidlo = brunhilda_snedl.objects.get(den=aktualni_den)
energie_jidlo = energie_bonus_jidlo.snedeno_energie

brunhilda_energie = ((energie_vcera)+(energie_jidlo)+(brunhilda_spanek*20)+(kcal_prijem_dnes/500)-(200)-(dnesni_prumer_kroku/1000))*((negace_energie_hydratace+negace_energie_sytost)/2)

brunhilda_energie_procenta = round(brunhilda_energie)

if brunhilda_energie<0.1:
    brunhilda_energie_procenta=0.1
if brunhilda_energie>150:
    brunhilda_energie_procenta=150

if brunhilda_energie_procenta <30:
    negace_kondice_energie = 0.95
elif brunhilda_energie_procenta <15:
    negace_kondice_energie=0.9
else:
    negace_kondice_energie=1

# KONDICE 

if hubnuti_nabirani > 3:
    kondice = 0
elif hubnuti_nabirani == 3:
    kondice = 5
elif hubnuti_nabirani > 2 and hubnuti_nabirani < 3:
    # Lineární interpolace mezi (3, 5) a (2, 40)
    kondice = 5 + (hubnuti_nabirani - 3) * (40 - 5) / (2 - 3)
elif hubnuti_nabirani == 2:
    kondice = 40
elif hubnuti_nabirani > 1 and hubnuti_nabirani < 2:
    # Lineární interpolace mezi (2, 40) a (1, 80)
    kondice = 40 + (hubnuti_nabirani - 2) * (80 - 40) / (1 - 2)
elif hubnuti_nabirani == 1:
    kondice = 75
elif hubnuti_nabirani > 0.5 and hubnuti_nabirani < 1:
    # Lineární interpolace mezi (1, 80) a (0.5, 100)
    kondice = 75 + (hubnuti_nabirani - 1) * (100 - 80) / (0.5 - 1)
elif hubnuti_nabirani == 0.5:
    kondice = 90
elif hubnuti_nabirani > 0 and hubnuti_nabirani < 0.5:
    # Lineární interpolace mezi (0.5, 100) a (0, 90)
    kondice = 90 + (hubnuti_nabirani - 0.5) * (90 - 100) / (0 - 0.5)
elif hubnuti_nabirani == 0:
    kondice = 90
elif hubnuti_nabirani > -0.5 and hubnuti_nabirani < 0:
    # Lineární interpolace mezi (0, 90) a (-0.5, 100)
    kondice = 90 + (hubnuti_nabirani - 0) * (100 - 90) / (-0.5 - 0)
elif hubnuti_nabirani == -0.5:
    kondice = 100
elif hubnuti_nabirani > -1 and hubnuti_nabirani < -0.5:
    # Lineární interpolace mezi (-0.5, 100) a (-1, 80)
    kondice = 100 + (hubnuti_nabirani - (-0.5)) * (80 - 100) / (-1 - (-0.5))
elif hubnuti_nabirani == -1:
    kondice = 80
elif hubnuti_nabirani > -2 and hubnuti_nabirani < -1:
    # Lineární interpolace mezi (-1, 80) a (-2, 40)
    kondice = 80 + (hubnuti_nabirani - (-1)) * (40 - 80) / (-2 - (-1))
elif hubnuti_nabirani == -2:
    kondice = 40
elif hubnuti_nabirani > -3 and hubnuti_nabirani < -2:
    # Lineární interpolace mezi (-2, 40) a (-3, 5)
    kondice = 40 + (hubnuti_nabirani - (-2)) * (5 - 40) / (-3 - (-2))
elif hubnuti_nabirani == -3:
    kondice = 5
else: # hubnuti_nabirani < -3
    kondice = 0


kondice_procenta = round((kondice_vcera/10)+((kondice)*negace_kondice_energie))

if kondice<0.1:
    kondice_procenta=0.1
if kondice>150:
    kondice_procenta=150


# VÝKON !!!
koeficient_energie = 1
koeficient_kondice = 1
koeficient_hydratace = 1
koeficient_sytosti = 1
koeficient_zateze = 1


energie_body = [
    (-100, 0.1),
    (0, 0.15),
    (20, 0.4),
    (40, 0.6),
    (60, 0.8),
    (80, 1),
    (100, 1.4),
    (115, 1.6),
    (130, 1.8),
    (150, 2)
]

hodnota = brunhilda_energie_procenta
for i in range(len(energie_body) - 1):
    x0, y0 = energie_body[i]
    x1, y1 = energie_body[i + 1]
    if x0 <= hodnota <= x1:
        koeficient_energie = y0 + (y1 - y0) * ((hodnota - x0) / (x1 - x0))
        break
else:
    if hodnota > energie_body[-1][0]:
        koeficient_energie = energie_body[-1][1]
    else:
        koeficient_energie = energie_body[0][1]

kondice_body = [
    (-100, 0.1),
    (0, 0.15),
    (20, 0.4),
    (40, 0.6),
    (60, 0.8),
    (80, 1),
    (100, 1.4),
    (115, 1.6),
    (130, 1.8),
    (150, 2)
]

hodnota = kondice_procenta
for i in range(len(kondice_body) - 1):
    x0, y0 = kondice_body[i]
    x1, y1 = kondice_body[i + 1]
    if x0 <= hodnota <= x1:
        koeficient_kondice = y0 + (y1 - y0) * ((hodnota - x0) / (x1 - x0))
        break
else:
    if hodnota > kondice_body[-1][0]:
        koeficient_kondice = kondice_body[-1][1]
    else:
        koeficient_kondice = kondice_body[0][1]

hydratace_body = [
    (-100, 0.2),
    (0, 0.3),
    (20, 0.5),
    (40, 0.7),
    (60, 0.9),
    (80, 1),
    (100, 1.1),
    (115, 1.05),
    (130, 0.9),
    (150, 0.8)
]

hodnota = hydratace_procenta
for i in range(len(hydratace_body) - 1):
    x0, y0 = hydratace_body[i]
    x1, y1 = hydratace_body[i + 1]
    if x0 <= hodnota <= x1:
        koeficient_hydratace = y0 + (y1 - y0) * ((hodnota - x0) / (x1 - x0))
        break
else:
    if hodnota > hydratace_body[-1][0]:
        koeficient_hydratace = hydratace_body[-1][1]
    else:
        koeficient_hydratace = hydratace_body[0][1]

sytost_body = [
    (-100, 0.2),
    (0, 0.3),
    (20, 0.5),
    (40, 0.7),
    (60, 0.9),
    (80, 1),
    (100, 1.1),
    (115, 1.05),
    (130, 0.9),
    (150, 0.8)
]

hodnota = sytost_procenta
for i in range(len(sytost_body) - 1):
    x0, y0 = sytost_body[i]
    x1, y1 = sytost_body[i + 1]
    if x0 <= hodnota <= x1:
        koeficient_sytost = y0 + (y1 - y0) * ((hodnota - x0) / (x1 - x0))
        break
else:
    if hodnota > sytost_body[-1][0]:
        koeficient_sytost = sytost_body[-1][1]
    else:
        koeficient_sytost = sytost_body[0][1]

zatez_body = [
    (-100, 1.2),
    (0, 1.1),
    (20, 1.05),
    (40, 1),
    (60, 0.95),
    (80, 0.9),
    (100, 0.85),
    (115, 0.8),
    (130, 0.7),
    (150, 0.6)
]

hodnota = zatez_procenta
for i in range(len(zatez_body) - 1):
    x0, y0 = zatez_body[i]
    x1, y1 = zatez_body[i + 1]
    if x0 <= hodnota <= x1:
        koeficient_zatez = y0 + (y1 - y0) * ((hodnota - x0) / (x1 - x0))
        break
else:
    if hodnota > zatez_body[-1][0]:
        koeficient_zatez = zatez_body[-1][1]
    else:
        koeficient_zatez = zatez_body[0][1]

volna_kapacita_body = [
    (-100, 0.5),
    (0, 0.8),
    (20, 0.85),
    (40, 0.9),
    (60, 1),
    (80, 1.1),
    (100, 1.2),
    (115, 1.2),
    (130, 1.2),
    (150, 1.2)
]

hodnota = volna_kapacita_procenta
for i in range(len(volna_kapacita_body) - 1):
    x0, y0 = volna_kapacita_body[i]
    x1, y1 = volna_kapacita_body[i + 1]
    if x0 <= hodnota <= x1:
        koeficient_volne_kapacity = y0 + (y1 - y0) * ((hodnota - x0) / (x1 - x0))
        break
else:
    if hodnota > volna_kapacita_body[-1][0]:
        koeficient_volne_kapacity = volna_kapacita_body[-1][1]
    else:
        koeficient_volne_kapacity = volna_kapacita_body[0][1]



vykon_procenta = round((((brunhilda_energie_procenta)*(koeficient_energie))+(negace_hubnuti_procenta)+((kondice_procenta)*(koeficient_kondice))+((koeficient_hydratace)*(hydratace_procenta))+((sytost_procenta)*(koeficient_sytosti))+((zatez_procenta)*(koeficient_zateze))+((volna_kapacita_procenta)*(koeficient_volne_kapacity)))/7) #<-- 7=počet atributů (děláme průměr)

vykon_konstanta = 1

if vykon_procenta > 150:
    vykon_konstanta = 1.6
elif vykon_procenta > 0:
    if vykon_procenta > 130:
        vykon_konstanta = 1.5 + (1.6 - 1.5) * (vykon_procenta - 130) / (150 - 130)
    elif vykon_procenta > 115:
        vykon_konstanta = 1.4 + (1.5 - 1.4) * (vykon_procenta - 115) / (130 - 115)
    elif vykon_procenta > 100:
        vykon_konstanta = 1.3 + (1.4 - 1.3) * (vykon_procenta - 100) / (115 - 100)
    elif vykon_procenta > 80:
        vykon_konstanta = 1.2 + (1.3 - 1.2) * (vykon_procenta - 80) / (100 - 80)
    elif vykon_procenta > 60:
        vykon_konstanta = 1.1 + (1.2 - 1.1) * (vykon_procenta - 60) / (80 - 60)
    elif vykon_procenta > 40:
        vykon_konstanta = 1.0 + (1.1 - 1.0) * (vykon_procenta - 40) / (60 - 40)
    elif vykon_procenta > 20:
        vykon_konstanta = 0.9 + (1.0 - 0.9) * (vykon_procenta - 20) / (40 - 20)
    else: # vykon_procenta > 0 and vykon_procenta <= 20
        vykon_konstanta = 0.75 + (0.9 - 0.75) * vykon_procenta / 20
elif vykon_procenta <= 0:
    vykon_konstanta = 0.5


# BRUNHILDA XP
XP_bonus_flat = round((suma_kroky/10000),1)*(BONUS_XP_flat)
xp_vcera = pamet_brunhilda.objects.get(den=vcerejsi_den)
xp_vcera_pamet = xp_vcera.aktual_XP

brunhilda_xp = round(((((suma_kroky/100)/(pocet_hracu_brunhilda))+(XP_bonus_flat))*BONUS_XP_procenta))
XP_DNES = brunhilda_xp-xp_vcera_pamet

#BRUNHILDA LVL
if brunhilda_xp <= 80:
    brunhilda_xp = 81
    XP_DNES = 81

lvl1 = 80
lvlkons = 2

lvl2 = round(lvl1+(lvl1/lvlkons))
lvl3 = lvl2+round((lvl2/lvlkons))
lvl4 = lvl3+round((lvl3/lvlkons))
lvl5 = lvl4+round((lvl4/lvlkons))
lvl6 = lvl5+round((lvl5/lvlkons))
lvl7 = lvl6+round((lvl6/lvlkons))
lvl8 = lvl7+round((lvl7/lvlkons))
lvl9 = lvl8+round((lvl8/lvlkons))
lvl10 = lvl9+round((lvl9/lvlkons))
lvl11 = lvl10+round((lvl10/lvlkons))
lvl12 = lvl11+round((lvl11/lvlkons))
lvl13 = lvl12+round((lvl12/lvlkons))
lvl14 = lvl13+round((lvl13/lvlkons))
lvl15 = lvl14+round((lvl14/lvlkons))
lvl16 = lvl15+round((lvl15/lvlkons))
lvl17 = lvl16+round((lvl16/lvlkons))
lvl18 = lvl17+round((lvl17/lvlkons))
lvl19 = lvl18+round((lvl18/lvlkons))
lvl20 = lvl19+round((lvl19/lvlkons))
lvl21 = lvl20+round((lvl20/lvlkons))
lvl22 = lvl21+round((lvl21/lvlkons))
lvl23 = lvl22+round((lvl22/lvlkons))
lvl24 = lvl23+round((lvl23/lvlkons))
lvl25 = lvl24+round((lvl24/lvlkons))
lvl26 = lvl25+round((lvl25/lvlkons))
lvl27 = lvl26+round((lvl26/lvlkons))
lvl28 = lvl27+round((lvl27/lvlkons))
lvl29 = lvl28+round((lvl28/lvlkons))
lvl30 = lvl29+round((lvl29/lvlkons))

# Objekt (slovník) obsahující všechny úrovně
levely = {
    "lvl30": int(lvl30),
    "lvl29": int(lvl29),
    "lvl28": int(lvl28),
    "lvl27": int(lvl27),
    "lvl26": int(lvl26),
    "lvl25": int(lvl25),
    "lvl24": int(lvl24),
    "lvl23": int(lvl23),
    "lvl22": int(lvl22),
    "lvl21": int(lvl21),
    "lvl20": int(lvl20),
    "lvl19": int(lvl19),
    "lvl18": int(lvl18),
    "lvl17": int(lvl17),
    "lvl16": int(lvl16),
    "lvl15": int(lvl15),
    "lvl14": int(lvl14),
    "lvl13": int(lvl13),
    "lvl12": int(lvl12),
    "lvl11": int(lvl11),
    "lvl10": int(lvl10),
    "lvl9": int(lvl9),
    "lvl8": int(lvl8),
    "lvl7": int(lvl7),
    "lvl6": int(lvl6),
    "lvl5": int(lvl5),
    "lvl4": int(lvl4),
    "lvl3": int(lvl3),
    "lvl2": int(lvl2),
    "lvl1": int(lvl1),
}

aktualni_lvl = 30

for lvl in levely.values():
    if brunhilda_xp > lvl:
        aktualni_lvl = aktualni_lvl
        next_lvl_jeste_chybi = xp_na_next_lvl-brunhilda_xp
        xp_next_lvl = ((brunhilda_xp)+(xp_na_next_lvl))-brunhilda_xp
    else:
        aktualni_lvl = aktualni_lvl-1
        xp_na_next_lvl = lvl

bonus_km_lvl = 1+(aktualni_lvl/20)

next_lvl_procenta = round(brunhilda_xp/(xp_next_lvl/100),1)

# INCOME PENÍZE
daily_income = (aktualni_den*200)+(BONUS_income_flat)
money_income = round(((daily_income)*(aktualni_lvl/3))*BONUS_income_procenta)

# HODNOTA INV
inv_cena = brunhilda_inv.objects.get(den=aktualni_den)
inv_suma_cena = inv_cena.cena_inv


brunhilda_final_km_vcera = pamet_brunhilda.objects.get(den=vcerejsi_den)
final_km_vcera = brunhilda_final_km_vcera.km_s_bonusem
BRUNHILDA_FINAL_KM = round((final_km_vcera+(((brunhilda_km_dnes*vykon_konstanta))*(bonus_km_lvl))),2)

brunhilda_km_bonus_dnes = round(((brunhilda_km_dnes*vykon_konstanta)*bonus_km_lvl),2)


if BONUS_delka_kroku_procenta != 0:
    BONUS_delka_kroku_procenta = round(((BONUS_delka_kroku_procenta-1)*100),1)
if BONUS_BMR_procenta != 0:
    BONUS_BMR_procenta = round(((BONUS_BMR_procenta-1)*100),1)
if BONUS_zatez_procenta != 0:
    BONUS_zatez_procenta = round(((BONUS_zatez_procenta-1)*100),1)
if BONUS_income_flat != 0:
    BONUS_income_flat = BONUS_income_flat
if BONUS_income_procenta != 0:
    BONUS_income_procenta = round(((BONUS_income_procenta-1)*100),1)
if BONUS_kapacita_flet != 0:
    BONUS_kapacita_flet = BONUS_kapacita_flet
if BONUS_kapacita_procenta != 0:
    BONUS_kapacita_procenta = round(((BONUS_kapacita_procenta-1)*100),1)
if BONUS_XP_flat != 0:
    BONUS_XP_flat = BONUS_XP_flat
if BONUS_XP_procenta != 0:
    BONUS_XP_procenta = round(((BONUS_XP_procenta-1)*100),1)
if BONUS_spanek_flat != 0:
    BONUS_spanek_flat = BONUS_spanek_flat
if BONUS_spanek_procenta != 0:
    BONUS_spanek_procenta = round(((BONUS_spanek_procenta-1)*100),1)
if BONUS_cena_procenta != 0:
    BONUS_cena_procenta = round(((BONUS_cena_procenta-1)*100),1)

# PŘEJMENOVÁNÍ:
brunhilda_kondice_procenta = kondice_procenta
brunhilda_sytost_procenta = sytost_procenta
brunhilda_hydratace_procenta = hydratace_procenta
brunhilda_zatez_procenta = zatez_procenta
brunhilda_volna_kapacita_procenta = volna_kapacita_procenta

def brunhilda_main_page(request):

    context = {}
    context['brunhilda_xp'] = brunhilda_xp
    context["aktualni_lvl"] = aktualni_lvl
    context['nasledujici_den'] = nasledujici_den
    context["xp_na_next_lvl"] = xp_na_next_lvl
    context['next_lvl_procenta'] = next_lvl_procenta
    context["money_income"] = money_income
# OBRÁZKY
    context['boty_img'] = boty_img
    context['ponozky_img'] = ponozky_img
    context['kalhoty_img'] = kalhoty_img
    context['triko_img'] = triko_img
    context['doplnek_img'] = doplnek_img
    context['batoh_img'] = batoh_img
    context['spacak_img'] = spacak_img
    context['karimatka_img'] = karimatka_img


# TO NEJDŮLEŽITĚJŠÍ:
    context['BRUNHILDA_FINAL_KROKY'] = BRUNHILDA_FINAL_KM

# HLAVNÍ STATY:
    context['vykon_procenta'] = vykon_procenta

    context['volna_kapacita_procenta'] = brunhilda_volna_kapacita_procenta
    context['zatez_procenta'] = brunhilda_zatez_procenta
    context['kondice_procenta'] = brunhilda_kondice_procenta
    context['brunhilda_energie_procenta'] = brunhilda_energie_procenta
    context['hydratace_procenta'] = brunhilda_hydratace_procenta
    context['sytost_procenta'] = brunhilda_sytost_procenta

    context['aktualni_den'] = aktualni_den
    context['denni_prumer_kroku'] = round(dnesni_prumer_kroku)
    context['brunhilda_km_dnes'] = brunhilda_km_dnes
    context['hubnuti_nabirani'] = hubnuti_nabirani

# OBRÁZKY

# VEDLEJŠÍ STATY:
    context['celkem_kroku'] = suma_kroky
    context['BMI'] = brunhilda_BMI
    context['brunhilda_km_dnes'] = brunhilda_km_dnes
    context['kcal_prijem_dnes'] = kcal_prijem_dnes
    context['kcal_vydej_dnes_SUMA'] = kcal_vydej_dnes_SUMA
    context['kcal_rozdil_dnes'] = kcal_rozdil_dnes
    context['kapacita'] = kapacita_batohu
    context['volna_kapacita'] = volna_kapacita
    context['tempo'] = tempo
    context['sum_kcal_dnes'] = kcal_prijem_dnes
    
# POMOCNÉ STATY:
    context['delka_kroku'] = zakladni_staty.delkakroku
    context['brunhilda_spanek'] = brunhilda_spanek
    context['brunhilda_aktivita'] = brunhilda_aktivita
    context['zatez'] = zatez
    context['brunhilda_bmr'] = brunhilda_BMR
    context['brunhilda_zakladni_vaha'] = zakladni_staty.vaha
    context['brunhilda_celkova_vaha'] = brunhilda_celkova_vaha
    context['brunhilda_vyska'] = zakladni_staty.vyska
    context['brunhilda_vek'] = zakladni_staty.vek
    context['brunhilda_pohlavi'] = zakladni_staty.pohlavi



    return render(request, 'brunhildaapp/brunhilda_main_page.html', context)


def full_tym(request):
    hraci = vysledky_hracu.objects.filter(tym="brunhilda")
    return render(request, 'brunhildaapp/brunhilda_full_tym.html', {
        'brunhilda_vsichni_hraci': hraci
    })


def leaderboard(request):
    return render(request, 'brunhildaapp/brunhilda_leaderboard.html', {
        'vsichni_hraci_brunhilda': hraci,
    })


def detail_hrace(request, id):
    tym_brunhilda = vysledky_hracu.objects.filter(tym="brunhilda")
    hracid = vysledky_hracu.objects.get(id=id)
    hracid.celkem_kroku = hracid.kroky1 + hracid.kroky2 + hracid.kroky3 + hracid.kroky4 + hracid.kroky5 + hracid.kroky6 + hracid.kroky7 + hracid.kroky8 + hracid.kroky9 + hracid.kroky10 + hracid.kroky11 + hracid.kroky12


# OSOBNÍ REKORD HRÁČE

    rekordID = vysledky_hracu.objects.get(id=id)
    rekord = rekordID.max_kroku_mesicne

# ZJIŠTĚNÍ CELKOVÉHO POŘADÍ HRÁČE

    try:
        IDporadi_hrace = vysledky_hracu.objects.get(id=id)
        vsichni_hraci = vysledky_hracu.objects.all().order_by('celkem_kroku')
        poradi = 1
        for hrac in vsichni_hraci:
            if IDporadi_hrace.celkem_kroku < hrac.celkem_kroku:
                poradi += 1
            else:
                pass
    except:
        pass

# ZJIŠTĚNÍ TÝMOVÉHO POŘADÍ HRÁČE
    try:
        IDporadi_hrace = vysledky_hracu.objects.get(id=id)
        tym_brunhilda = vysledky_hracu.objects.filter(tym="brunhilda").order_by('celkem_kroku')
        poradi_v_tymu = 0
        for hrac in tym_brunhilda:
            if IDporadi_hrace.celkem_kroku <= hrac.celkem_kroku:
                poradi_v_tymu += 1
            else:
                pass
  
    except:
        pass

    kroky_celkem = (hracid.celkem_kroku)+(hracid.kroky_BONUS)

    kroky_list = [
        hracid.kroky1,
        hracid.kroky2,
        hracid.kroky3,
        hracid.kroky4,
        hracid.kroky5,
        hracid.kroky6,
        hracid.kroky7,
        hracid.kroky8,
        hracid.kroky9,
        hracid.kroky10,
        hracid.kroky11,
        hracid.kroky12,
    ]
    motivacni_citaty = [
    "Nejlepší způsob, jak začít, je přestat mluvit a začít dělat. - Walt Disney",
    "Váš čas je omezený, tak ho neztrácejte životem někoho jiného. - Steve Jobs",
    "Pokud chcete žít šťastný život, spojte ho s cílem, ne s lidmi nebo věcmi. - Albert Einstein",
    "Neúspěch je jen příležitost začít znovu, tentokrát inteligentněji. - Henry Ford",
    "Jediným místem, kde úspěch předchází práci, je ve slovníku. - Vidal Sassoon",
    "Věřte, že můžete, a jste v polovině cesty. - Theodore Roosevelt",
    "Abychom uspěli, musíme nejprve věřit, že můžeme. - Nikos Kazantzakis",
    "Cesta dlouhá tisíc mil začíná jediným krokem. - Lao Tzu",
    "Není důležité, jak pomalu jdete, dokud nezastavíte. - Konfucius",
    "Vaše jediná omezení jsou ta, která si sami stanovíte. - Napoleon Hill",
    "Úspěch není konečný, neúspěch není fatální: Důležitá je odvaha pokračovat. - Winston Churchill",
    "Co si mysl dokáže představit a čemu dokáže uvěřit, toho může dosáhnout. - Napoleon Hill",
    "Snažte se nebýt úspěchem, ale spíše hodnotou. - Albert Einstein",
    "Dva nejdůležitější dny ve vašem životě jsou den, kdy jste se narodili, a den, kdy zjistíte proč. - Mark Twain",
    "Nejlepší pomsta je masivní úspěch. - Frank Sinatra",
    "Já jsem selhal znovu a znovu a znovu v mém životě. A proto uspěji. - Michael Jordan",
    "Sny se neplní samy od sebe. Musíte na nich pracovat. - Colin Powell",
    "Stanovte si vysoké cíle a nezastavujte se, dokud se tam nedostanete. - Bo Jackson",
    "Překážky jsou ty děsivé věci, které vidíte, když odvrátíte zrak od svého cíle. - Henry Ford",
    "Jediný způsob, jak dělat skvělou práci, je milovat to, co děláte. - Steve Jobs",
    "Pokud procházíte peklem, pokračujte. - Winston Churchill",
    "Tvrdá práce porazí talent, když talent nepracuje tvrdě. - Tim Notke",
    "Buďte změnou, kterou chcete vidět ve světě. - Mahátma Gándhí",
    "Vítězové se nikdy nevzdávají a ti, co se vzdávají, nikdy nevítězí. - Vince Lombardi",
    "Jste odvážnější, než věříte, silnější, než se zdáte, a chytřejší, než si myslíte. - A. A. Milne",
    "Nikdy není pozdě být tím, kým jste mohli být. - George Eliot",
    "Když něco opravdu chcete, celý vesmír se spojí, abyste toho dosáhli. - Paulo Coelho",
    "Štěstí není něco hotového. Přichází z vašich vlastních činů. - Dalajláma",
    "Nečekejte. Čas nikdy nebude ten správný. - Napoleon Hill",
    "Budoucnost patří těm, kdo věří v krásu svých snů. - Eleanor Roosevelt",
    "Akce je základním klíčem k veškerému úspěchu. - Pablo Picasso",
    "Musíte dělat věci, o kterých si myslíte, že je nemůžete dělat. - Eleanor Roosevelt",
    "Jediný limit k našemu uskutečnění zítřka budou naše dnešní pochybnosti. - Franklin D. Roosevelt",
    "Pokud si dokážete něco vysnít, dokážete to i udělat. - Walt Disney",
    "Za dvacet let budete více zklamáni věcmi, které jste neudělali, než těmi, které jste udělali. - Mark Twain",
    "Naše největší sláva nespočívá v tom, že nikdy nepadneme, ale v tom, že vstaneme pokaždé, když padneme. - Konfucius",
    "Rozdíl mezi obyčejným a neobyčejným je to malé 'navíc'. - Jimmy Johnson",
    "Váš přístup, ne vaše schopnosti, určí vaši výšku. - Zig Ziglar",
    "Pokud nemůžete dělat velké věci, dělejte malé věci skvělým způsobem. - Napoleon Hill",
    "Odvaha je odolnost vůči strachu, zvládnutí strachu – nikoli absence strachu. - Mark Twain",
    "Problémy nejsou stopkami, jsou to ukazatelé směru. - Robert H. Schuller",
    "Vždy se zdá nemožné, dokud to není hotové. - Nelson Mandela",
    "Začněte tam, kde jste. Použijte to, co máte. Dělejte to, co můžete. - Arthur Ashe",
    "Neúspěch je kořením, které dává úspěchu jeho chuť. - Truman Capote",
    "Nic není nemožné, slovo samo říká 'Jsem možný'! (I'm possible) - Audrey Hepburn",
    "Mějte velké sny a odvažte se selhat. - Norman Vaughan",
    "Nejlepší čas zasadit strom byl před 20 lety. Druhý nejlepší čas je teď. - Čínské přísloví",
    "Úspěch obvykle přichází k těm, kteří jsou příliš zaneprázdněni na to, aby ho hledali. - Henry David Thoreau",
    "Nenechte včerejšek zabrat příliš mnoho z dneška. - Will Rogers",
    "Inovace rozlišuje mezi lídrem a následovníkem. - Steve Jobs"
]
    delka_seznamu = len(motivacni_citaty)
    nahodny_index = random.randint(0, delka_seznamu - 1)
    nahodny_citat = motivacni_citaty[nahodny_index]


    
    return render(request, 'brunhildaapp/brunhilda_detail_hrace.html', {
        'brunhilda_vsichni_hraci': pocet_hracu_brunhilda,
        'celkove_poradi': poradi,
        'poradi_v_tymu': poradi_v_tymu,
        'pocet_hracu_pepa': pocet_hracu_pepa,
        'pocet_hracu_karel': pocet_hracu_karel,
        'pocet_hracu_brunhilda': pocet_hracu_brunhilda,
        'pocet_hracu_CELKEM': pocet_hracu_celkem,
        'kroky_BONUS': hracid.kroky_BONUS,
        'kroky_list': kroky_list,
        'kroky_celkem': kroky_celkem,
        'rekord': rekord,
        'tym': hracid.tym,
        'jmeno': hracid.jmeno,
        'prijmeni': hracid.prijmeni,
        'random_citat': nahodny_citat
    })

brunhilda_pamet = pamet_brunhilda.objects.all()


def detail_statistika(request):
    context = {}
    context['nasledujici_den'] = nasledujici_den
    context['brunhilda_xp'] = brunhilda_xp
    context["xp_na_next_lvl"] = xp_na_next_lvl
    context['aktualni_den'] = aktualni_den
    context['denni_prumer_kroku'] = round(dnesni_prumer_kroku)
    context['hubnuti_nabirani'] = hubnuti_nabirani
    context['celkem_kroku'] = suma_kroky
    context['BMI'] = brunhilda_BMI
    context['kcal_prijem_dnes'] = kcal_prijem_dnes
    context['kcal_vydej_dnes_SUMA'] = kcal_vydej_dnes_SUMA
    context['kcal_rozdil_dnes'] = kcal_rozdil_dnes
    context['kapacita'] = kapacita_batohu
    context['volna_kapacita'] = volna_kapacita
    context['tempo'] = tempo
    context['brunhilda_bmr'] = brunhilda_BMR
    context['vcerejsi_den'] = vcerejsi_den
    context['aktivita'] = aktivita_dnes.brunhilda_aktivita
    context['brunhilda_km_dnes'] = brunhilda_km_dnes
    context['brunhilda_km_bez_bonusu'] = brunhilda_km_bonus_dnes
    context['brunhilda_celkova_vaha'] = brunhilda_celkova_vaha
    context['XP_DNES'] = XP_DNES
    context['BRUNHILDA_FINAL_KM'] = BRUNHILDA_FINAL_KM
    context['BONUS_delka_kroku_procenta'] = BONUS_delka_kroku_procenta
    context['BONUS_BMR_procenta'] = BONUS_BMR_procenta
    context['BONUS_zatez_procenta'] = BONUS_zatez_procenta
    context['BONUS_income_flat'] = BONUS_income_flat
    context['BONUS_income_procenta'] = BONUS_income_procenta
    context['BONUS_kapacita_flet'] = BONUS_kapacita_flet
    context['BONUS_kapacita_procenta'] = BONUS_kapacita_procenta
    context['BONUS_XP_flat'] = BONUS_XP_flat
    context['BONUS_XP_procenta'] = BONUS_XP_procenta
    context['BONUS_spanek_flat'] = BONUS_spanek_flat
    context['BONUS_spanek_procenta'] = BONUS_spanek_procenta
    context['BONUS_cena_procenta'] = BONUS_cena_procenta


    return render(request, 'brunhildaapp/brunhilda_detail_statistika.html', context)




def jednotlive_dny(request):
    return render(request, 'brunhildaapp/brunhilda_jednotlive_dny.html', {
        'brunhilda_pamet': brunhilda_pamet,
    })