from django.contrib import admin
from .models import vysledky_hracu
from django import forms
from django.contrib import admin

class vysledky_hracuAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()  # Spustí přepsanou metodu save()


admin.site.register(vysledky_hracu, vysledky_hracuAdmin)
