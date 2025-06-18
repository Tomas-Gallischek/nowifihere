from django import forms
from django.contrib import admin
from adminapp.models import aktualniden, food_drink, vybava, aktivita_kcal2, kondice_hubnuti, spanek
from .models import brunhilda_zakladni_staty, brunhilda_snedl, brunhilda_snedl_polozka, brunhilda_equip, InventarPolozkaFood, InventarPolozkaVybava, brunhilda_inv

class brunhilda_zakladni_statyAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()  # Spustí přepsanou metodu save()

admin.site.register(brunhilda_zakladni_staty, brunhilda_zakladni_statyAdmin)


# BRUNHILDA SNĚDL
class BrunhildaSnedlPolozkaInline(admin.TabularInline):
    model = brunhilda_snedl_polozka
    extra = 2  # Počet prázdných formulářů pro přidání dalších položek

@admin.register(brunhilda_snedl)
class BrunhildaSnedlAdmin(admin.ModelAdmin):
    inlines = [BrunhildaSnedlPolozkaInline]


# BRUNHILDA Equip

class BrunhildaEquipForm(forms.ModelForm):
    equip_boty = forms.ModelChoiceField(
        queryset=vybava.objects.none(),  # Start with empty queryset
        required=False,
        label='Boty'
    )
    equip_ponozky = forms.ModelChoiceField(
        queryset=vybava.objects.none(),
        required=False,
        label='Ponožky'
    )
    equip_kalhoty = forms.ModelChoiceField(
        queryset=vybava.objects.none(),
        required=False,
        label='Kalhoty'
    )
    equip_triko = forms.ModelChoiceField(
        queryset=vybava.objects.none(),
        required=False,
        label='Triko'
    )
    equip_doplnek = forms.ModelChoiceField(
        queryset=vybava.objects.none(),
        required=False,
        label='Doplněk'
    )
    equip_batoh = forms.ModelChoiceField(
        queryset=vybava.objects.none(),
        required=False,
        label='Batoh'
    )
    equip_spacak = forms.ModelChoiceField(
        queryset=vybava.objects.none(),
        required=False,
        label='Spacák'
    )
    equip_karimatka = forms.ModelChoiceField(
        queryset=vybava.objects.none(),
        required=False,
        label='Karimatka'
    )

    class Meta:
        model = brunhilda_equip
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            den = self.instance.den
        else:
            den = self.data.get('den')

        if den:
            try:
                brunhilda_inventory = brunhilda_inv.objects.get(den=den)

                # Get the items in Brunhilda's inventory
                inventory_item_ids = brunhilda_inventory.vybaveni.values_list('polozka_id', flat=True)
                available_vybava_items = vybava.objects.filter(id__in=inventory_item_ids)

                # Populate the querysets for the form fields
                self.fields['equip_boty'].queryset = available_vybava_items.filter(item_typ='boty')
                self.fields['equip_ponozky'].queryset = available_vybava_items.filter(item_typ='ponozky')
                self.fields['equip_kalhoty'].queryset = available_vybava_items.filter(item_typ='kalhoty')
                self.fields['equip_triko'].queryset = available_vybava_items.filter(item_typ='triko')
                self.fields['equip_doplnek'].queryset = available_vybava_items.filter(item_typ='doplnek')
                self.fields['equip_batoh'].queryset = available_vybava_items.filter(item_typ='batoh')
                self.fields['equip_spacak'].queryset = available_vybava_items.filter(item_typ='spacak')
                self.fields['equip_karimatka'].queryset = available_vybava_items.filter(item_typ='karimatka')

            except brunhilda_inv.DoesNotExist:
                # Handle the case where there's no inventory for the current day
                # You might want to log this or provide a user-friendly message
                pass
class BrunhildaEquipAdmin(admin.ModelAdmin):
    form = BrunhildaEquipForm

admin.site.register(brunhilda_equip, BrunhildaEquipAdmin)

# BRUNHILDA INVENTÁŘ
class InventarPolozkaFoodInline(admin.TabularInline):
    model = InventarPolozkaFood
    extra = 1

class InventarPolozkaVybavaInline(admin.TabularInline):
    model = InventarPolozkaVybava
    extra = 1

@admin.register(brunhilda_inv)
class BrunhildaInvAdmin(admin.ModelAdmin):
    inlines = [InventarPolozkaFoodInline, InventarPolozkaVybavaInline]
    

    def save_related(self, request, form, formsets, change):
        """
        Po uložení hlavního objektu a souvisejících inline objektů
        spočítáme a uložíme celkovou váhu a objem inventáře.
        """
        super().save_related(request, form, formsets, change)
        instance = form.instance
        celkova_vaha = 0
        celkovy_objem = 0
        celkova_cena = 0

        for polozka in instance.potraviny.all():
            celkova_vaha += polozka.polozka.food_vaha * polozka.mnozstvi
            celkovy_objem += polozka.polozka.food_objem * polozka.mnozstvi
            celkova_cena += polozka.polozka.food_cena * polozka.mnozstvi

        for polozka in instance.vybaveni.all():
            celkova_vaha += polozka.polozka.item_vaha * polozka.mnozstvi
            celkovy_objem += polozka.polozka.item_objem
            celkova_cena += polozka.polozka.item_cena * polozka.mnozstvi

        instance.vaha_inventare = celkova_vaha
        instance.objem_inventare = celkovy_objem
        instance.cena_inv = celkova_cena
        instance.save()