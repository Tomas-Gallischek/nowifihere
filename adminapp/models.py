from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class aktualniden(models.Model):
    cislo_dne = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(12)])

    def __str__(self):
        return f'den č:{self.cislo_dne}'
    class Meta:
        verbose_name = "Přepnout den"
        verbose_name_plural = "Přepnout den"

class food_drink(models.Model):
    food_img = models.ImageField(upload_to='food_images/', blank=True)
    food_name = models.CharField(max_length=1000)
    food_znacka = models.CharField(max_length=1000)
    food_typ = models.CharField(max_length=1000)
    food_vaha = models.FloatField(max_length=1000, default=0)
    food_objem = models.FloatField(max_length=1000, default=0)
    food_kcal = models.FloatField(max_length=1000, default=0)
    food_sytost = models.FloatField(max_length=1000, default=0)
    food_hydratace = models.FloatField(max_length=1000, default=0)
    food_cena = models.FloatField(max_length=1000, default=0)
    food_energie = models.FloatField(max_length=1000, default=0, blank=True)

    def __str__(self):
        return f'{self.food_typ} - {self.food_name}'

    class Meta:
        verbose_name = "Databáze: Jídlo + pití"
        verbose_name_plural = "Databáze: Jídlo + pití"


class vybava(models.Model):
    item_img = models.ImageField(upload_to='item_images/', blank=True)
    item_name = models.CharField(max_length=1000, )
    item_znacka = models.CharField(max_length=1000, )
    item_typ = models.CharField(max_length=1000, )
    item_vaha = models.FloatField(max_length=1000, default=0)
    item_objem = models.FloatField(max_length=1000, default=0)
    item_bonus_delka_kroku_procenta = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_BMR_procenta = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_zatez_procenta = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_income_FLAT = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_income_procenta = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_kapacita_FLAT = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_kapacita_procenta = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_XP_procenta = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_XP_FLAT = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_spanek_FLAT = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_spanek_procenta = models.FloatField(max_length=1000, default=0, blank=True)
    item_bonus_cena_procenta = models.FloatField(max_length=1000, default=0, blank=True)
    item_cena = models.FloatField(max_length=1000, default=0)
    item_pozn = models.CharField(max_length=1000, default=item_name)

    def __str__(self):
        return f'{self.item_name}'

    class Meta:
        verbose_name = "Databáze: Výbava"
        verbose_name_plural = "Databáze: Výbava"


class aktivita_kcal2(models.Model):
    tempo = models.FloatField()
    kcal_za_hodinu = models.IntegerField()

    class Meta:
        verbose_name = "ÝPOČET kcal/h"
        verbose_name_plural = "ÝPOČET kcal/h"

    
class kondice_hubnuti(models.Model):
    hubnuti = models.FloatField()
    hubnuti_kondice = models.IntegerField()

    class Meta:
        verbose_name = "Hubnutí - kondice"
        verbose_name_plural = "Hubnutí - kondice"


class spanek(models.Model):
    den = models.IntegerField()
    pepa_spanek = models.IntegerField(default=0, validators=[MaxValueValidator(12)])
    karel_spanek = models.IntegerField(default=0, validators=[MaxValueValidator(12)])
    brunhilda_spanek = models.IntegerField(default=0, validators=[MaxValueValidator(12)])
    pepa_aktivita = models.IntegerField(default=0)
    karel_aktivita = models.IntegerField(default=0)
    brunhilda_aktivita = models.IntegerField(default=0)
    pozn = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.pepa_aktivita = 16 - self.pepa_spanek
        self.karel_aktivita = 16 - self.karel_spanek
        self.brunhilda_aktivita = 16 - self.brunhilda_spanek
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'den č:{self.den}'
    
    class Meta:
        verbose_name = "Kolik kdo spal"
        verbose_name_plural = "Kolik kdo spal"


class hraci_v_tymu(models.Model):
    pocet_hracu_pepa = models.IntegerField(default=0, blank=True)
    pocet_hracu_karel = models.IntegerField(default=0, blank=True)
    pocet_hracu_brunhilda = models.IntegerField(default=0, blank=True)
    hraci_celkem = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        self.hraci_celkem = (self.pocet_hracu_brunhilda)+(self.pocet_hracu_karel)+(self.pocet_hracu_pepa)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Počet hráčů v týmech"
        verbose_name_plural = "Počet hráčů v týmech"


class pamet_pepa(models.Model):
    den = models.IntegerField(blank=True)
    energie = models.IntegerField(blank=True)
    kondice = models.IntegerField(blank=True)
    hydratace = models.IntegerField(blank=True)
    sytost = models.IntegerField(blank=True)
    volna_kapacita = models.FloatField(blank=True)
    zatez = models.IntegerField(blank=True)
    pepova_aktualni_vaha = models.FloatField(default=0, blank=True)

    km_s_bonusem = models.FloatField(default=0, blank=True)
    aktual_XP = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return f'DEN:{self.den} - Energie:{self.energie}%, Kondice:{self.kondice}%, hydratace:{self.hydratace}%, Sytost:{self.sytost}%, Zátěž:{self.zatez}%, V.K.:{self.volna_kapacita}%, Aktuální váha:{self.pepova_aktualni_vaha}kg, Celkem KM:{self.km_s_bonusem}'
    
    class Meta:
        verbose_name = "Paměť - PEPA"
        verbose_name_plural = "Paměť - PEPA"

class pamet_karel(models.Model):
    den = models.IntegerField(blank=True)
    energie = models.IntegerField(blank=True)
    kondice = models.IntegerField(blank=True)
    hydratace = models.IntegerField(blank=True)
    sytost = models.IntegerField(blank=True)
    volna_kapacita = models.FloatField(blank=True)
    zatez = models.IntegerField(blank=True)
    pepova_aktualni_vaha = models.FloatField(default=0, blank=True)

    km_s_bonusem = models.FloatField(default=0, blank=True)
    aktual_XP = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return f'DEN:{self.den} - Energie:{self.energie}%, Kondice:{self.kondice}%, hydratace:{self.hydratace}%, Sytost:{self.sytost}%, Zátěž:{self.zatez}%, V.K.:{self.volna_kapacita}%, Aktuální váha:{self.pepova_aktualni_vaha}kg, Celkem KM:{self.km_s_bonusem}'
    
    class Meta:
        verbose_name = "Paměť - KAREL"
        verbose_name_plural = "Paměť - KAREL"

class pamet_brunhilda(models.Model):
    den = models.IntegerField(blank=True)
    energie = models.IntegerField(blank=True)
    kondice = models.IntegerField(blank=True)
    hydratace = models.IntegerField(blank=True)
    sytost = models.IntegerField(blank=True)
    volna_kapacita = models.FloatField(blank=True)
    zatez = models.IntegerField(blank=True)
    pepova_aktualni_vaha = models.FloatField(default=0, blank=True)

    km_s_bonusem = models.FloatField(default=0, blank=True)
    aktual_XP = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return f'DEN:{self.den} - Energie:{self.energie}%, Kondice:{self.kondice}%, hydratace:{self.hydratace}%, Sytost:{self.sytost}%, Zátěž:{self.zatez}%, V.K.:{self.volna_kapacita}%, Aktuální váha:{self.pepova_aktualni_vaha}kg, Celkem KM:{self.km_s_bonusem}'
    
    class Meta:
        verbose_name = "Paměť - BRUNHILDA"
        verbose_name_plural = "Paměť - BRUNHILDA"


class motivacni_citat(models.Model):
    citat = models.CharField(max_length=1000, blank=True)