from django.contrib import admin
from django import forms
from .models import aktualniden, food_drink, vybava, aktivita_kcal2, kondice_hubnuti, spanek, hraci_v_tymu, pamet_pepa
from pepaapp.models import pepa_zakladni_staty, pepa_snedl, pepa_snedl_polozka, pepa_equip, InventarPolozkaFood, InventarPolozkaVybava, pepa_inv

# AKTUÁLNÍ DEN
class aktualnidenAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
admin.site.register(aktualniden)

# JÍDLO + PITÍ
class food_drinkAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
admin.site.register(food_drink)

# VÝBAVA
class vybavaAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
admin.site.register(vybava)

# SPÁNEK
class spanekAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
admin.site.register(spanek)


# kcal/h
class aktivita_kcal2Admin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
admin.site.register(aktivita_kcal2)


#HRACI V TÝMU
class hraci_v_tymuAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
admin.site.register(hraci_v_tymu, hraci_v_tymuAdmin)

# PAMĚŤ
class pamet_pepaAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
admin.site.register(pamet_pepa, pamet_pepaAdmin)

