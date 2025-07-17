from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.db.models import Avg, Sum
from adminapp.models import food_drink, vybava

class karel_zakladni_staty(models.Model):
    jmeno = models.CharField(max_length=10)
    vek = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    vyska = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(300)])
    vaha = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(200)])
    pohlavi = models.CharField(max_length=10)
    delkakroku = models.FloatField(default=0)
    
    def __str__(self):
        return f'{self.jmeno} - ZÁKLADNÍ staty'
    
    class Meta:
        verbose_name = "KAREL - Základní staty"
        verbose_name_plural = "KAREL - Základní staty"

class karel_snedl(models.Model):
    den = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    snedeno_kcal = models.FloatField(default=0, blank=True)
    snedeno_sytost = models.FloatField(default=0, blank=True)
    snedeno_hydratace = models.FloatField(default=0, blank=True)
    snedeno_hmotnost = models.FloatField(default=0, blank=True)
    snedeno_energie = models.FloatField(default=0, blank=True, max_length=1000)

    def aktualizuj_souhrnne_hodnoty(self):
        """Spočítá a uloží souhrnné hodnoty z souvisejících položek."""
        celkem_kcal = 0
        celkem_sytost = 0
        celkem_hydratace = 0
        celkem_hmotnost = 0
        celkem_energie = 0
        for polozka in self.polozky.all():
            celkem_kcal += polozka.snedeno_kcal
            celkem_sytost += polozka.snedeno_sytost
            celkem_hydratace += polozka.snedeno_hydratace
            celkem_hmotnost += polozka.snedeno_hmotnost
            celkem_energie += polozka.snedeno_energie

        self.snedeno_kcal = celkem_kcal
        self.snedeno_sytost = celkem_sytost
        self.snedeno_hydratace = celkem_hydratace
        self.snedeno_hmotnost = celkem_hmotnost
        self.snedeno_energie = celkem_energie
        self.save()

    class Meta:
        verbose_name = "Co Karel snědl"
        verbose_name_plural = "Co Karel snědl"

    def __str__(self):
        return f'{self.den} - {self.snedeno_kcal}kcal'

class karel_snedl_polozka(models.Model):
    den = models.IntegerField(default=1, blank=True)
    karel_snedl = models.ForeignKey(karel_snedl, on_delete=models.CASCADE, related_name='polozky')
    # OPRAVA: Přidán unikátní related_name
    jidlo = models.ForeignKey('adminapp.food_drink', on_delete=models.CASCADE, related_name='karel_snedl_polozka')
    mnozstvi = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    snedeno_kcal = models.FloatField(default=0, blank=True)
    snedeno_sytost = models.FloatField(default=0, blank=True)
    snedeno_hydratace = models.FloatField(default=0, blank=True)
    snedeno_hmotnost = models.FloatField(default=0, blank=True)
    snedeno_energie = models.FloatField(default=0, blank=True, max_length=1000)

    def save(self, *args, **kwargs):
        """Před uložením zkopírujeme hodnoty z vybraného jídla a aktualizujeme souhrn."""
        self.snedeno_kcal = ((self.jidlo.food_kcal) * (self.mnozstvi))
        self.snedeno_sytost = ((self.jidlo.food_sytost)) * (self.mnozstvi)
        self.snedeno_hydratace = ((self.jidlo.food_hydratace)) * (self.mnozstvi)
        self.snedeno_hmotnost = ((self.jidlo.food_vaha)) * (self.mnozstvi)
        self.snedeno_energie = ((self.jidlo.food_energie)) * (self.mnozstvi)
        self.den = self.karel_snedl.den
        super().save(*args, **kwargs)
        self.karel_snedl.aktualizuj_souhrnne_hodnoty()

    def __str__(self):
        return f'{self.mnozstvi}x {self.jidlo.food_name}'

class karel_equip(models.Model):
    den = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    # OPRAVA: Všechny related_name jsou nyní unikátní pro 'karelapp'
    equip_boty = models.ForeignKey('adminapp.vybava', on_delete=models.CASCADE, related_name='karel_equip_boty', null=True, blank=True)
    equip_ponozky = models.ForeignKey('adminapp.vybava', on_delete=models.CASCADE, related_name='karel_equip_ponozky', null=True, blank=True)
    equip_kalhoty = models.ForeignKey('adminapp.vybava', on_delete=models.CASCADE, related_name='karel_equip_kalhoty', null=True, blank=True)
    equip_triko = models.ForeignKey('adminapp.vybava', on_delete=models.CASCADE, related_name='karel_equip_triko', null=True, blank=True)
    equip_doplnek = models.ForeignKey('adminapp.vybava', on_delete=models.CASCADE, related_name='karel_equip_doplnek', null=True, blank=True)
    equip_batoh = models.ForeignKey('adminapp.vybava', on_delete=models.CASCADE, related_name='karel_equip_batoh', null=True, blank=True)
    equip_spacak = models.ForeignKey('adminapp.vybava', on_delete=models.CASCADE, related_name='karel_equip_spacak', null=True, blank=True)
    equip_karimatka = models.ForeignKey('adminapp.vybava', on_delete=models.CASCADE, related_name='karel_equip_karimatka', null=True, blank=True)
    equip_pozn = models.CharField(max_length=1000, null=True, blank=True)
    equip_zatez = models.FloatField(default=0, null=True, blank=True)
    equip_objem = models.FloatField(default=0, null=True, blank=True)
    equip_cena = models.FloatField(default=0, blank=True)
    equip_BONUS_delka_kroku_procenta = models.FloatField(default=0, blank=True)
    equip_BONUS_BMR_procenta = models.FloatField(default=0, blank=True)
    equip_BONUS_zatez_procenta = models.FloatField(default=0, blank=True)
    equip_BONUS_income_flat = models.FloatField(default=0, blank=True)
    equip_BONUS_income_procenta = models.FloatField(default=0, blank=True)
    equip_BONUS_kapacita_flet = models.FloatField(default=0, blank=True)
    equip_BONUS_kapacita_procenta = models.FloatField(default=0, blank=True)
    equip_BONUS_XP_flat = models.FloatField(default=0, blank=True)
    equip_BONUS_XP_procenta = models.FloatField(default=0, blank=True)
    equip_BONUS_spanek_flat = models.FloatField(default=0, blank=True)
    equip_BONUS_spanek_procenta = models.FloatField(default=0, blank=True)
    equip_BONUS_cena_procenta = models.FloatField(default=0, blank=True)

    def __str__(self):
        return f'Den č: {self.den}: {self.equip_boty}, {self.equip_ponozky}, {self.equip_kalhoty}, {self.equip_triko}, {self.equip_doplnek}, {self.equip_batoh}, {self.equip_spacak}, {self.equip_karimatka}'

    def save(self, *args, **kwargs):
        celkova_zatez = 0
        celkovy_objem = 0
        cena = 0
        BONUS_delka_kroku_procenta = 0
        BONUS_BMR_procenta = 0
        BONUS_zatez_procenta = 0
        BONUS_income_flat = 0
        BONUS_income_procenta = 0
        BONUS_kapacita_flet = 0
        BONUS_kapacita_procenta = 0
        BONUS_XP_flat = 0
        BONUS_XP_procenta = 0
        BONUS_spanek_flat = 0
        BONUS_spanek_procenta = 0
        BONUS_cena_procenta = 0

        vybava_list = [
            self.equip_boty, self.equip_ponozky, self.equip_kalhoty, self.equip_triko,
            self.equip_doplnek, self.equip_batoh, self.equip_spacak, self.equip_karimatka
        ]

        for item in vybava_list:
            if item:
                celkova_zatez += item.item_vaha
                celkovy_objem += item.item_objem
                cena += item.item_cena
                BONUS_delka_kroku_procenta += item.item_bonus_delka_kroku_procenta
                BONUS_BMR_procenta += item.item_bonus_BMR_procenta
                BONUS_zatez_procenta += item.item_bonus_zatez_procenta
                BONUS_income_flat += item.item_bonus_income_FLAT
                BONUS_income_procenta += item.item_bonus_income_procenta
                BONUS_kapacita_flet += item.item_bonus_kapacita_FLAT
                BONUS_kapacita_procenta += item.item_bonus_kapacita_procenta
                BONUS_XP_flat += item.item_bonus_XP_FLAT
                BONUS_XP_procenta += item.item_bonus_XP_procenta
                BONUS_spanek_flat += item.item_bonus_spanek_FLAT
                BONUS_spanek_procenta += item.item_bonus_spanek_procenta
                BONUS_cena_procenta += item.item_bonus_cena_procenta

        self.equip_zatez = celkova_zatez
        self.equip_objem = celkovy_objem
        self.equip_cena = cena
        self.equip_BONUS_delka_kroku_procenta = BONUS_delka_kroku_procenta
        self.equip_BONUS_BMR_procenta = BONUS_BMR_procenta
        self.equip_BONUS_zatez_procenta = BONUS_zatez_procenta
        self.equip_BONUS_income_flat = BONUS_income_flat
        self.equip_BONUS_income_procenta = BONUS_income_procenta
        self.equip_BONUS_kapacita_flet = BONUS_kapacita_flet
        self.equip_BONUS_kapacita_procenta = BONUS_kapacita_procenta
        self.equip_BONUS_XP_flat = BONUS_XP_flat
        self.equip_BONUS_XP_procenta = BONUS_XP_procenta
        self.equip_BONUS_spanek_flat = BONUS_spanek_flat
        self.equip_BONUS_spanek_procenta = BONUS_spanek_procenta
        self.equip_BONUS_cena_procenta = BONUS_cena_procenta
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Co má Karel na sobě"
        verbose_name_plural = "Co má Karel na sobě"

# OBSAH INVENTÁŘE - JÍDLO
class InventarPolozkaFood(models.Model):
    inventar = models.ForeignKey('karel_inv', on_delete=models.CASCADE, related_name='potraviny')
    # OPRAVA: Přidán unikátní related_name
    polozka = models.ForeignKey('adminapp.food_drink', on_delete=models.CASCADE, related_name='karel_inventar_food')
    mnozstvi = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.mnozstvi}x {self.polozka.food_name} v inventáři pro den {self.inventar.den}'

# OBSAH INVENTÁŘE - VYBAVENÍ
class InventarPolozkaVybava(models.Model):
    inventar = models.ForeignKey('karel_inv', on_delete=models.CASCADE, related_name='vybaveni')
    # OPRAVA: Přidán unikátní related_name
    polozka = models.ForeignKey('adminapp.vybava', on_delete=models.CASCADE, related_name='karel_inventar_vybava')
    mnozstvi = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.mnozstvi}x {self.polozka.item_name} v inventáři pro den {self.inventar.den}'

class karel_inv(models.Model):
    den = models.IntegerField(validators=[MinValueValidator(0)], null=True, unique=True)
    vaha_inventare = models.FloatField(default=1)
    objem_inventare = models.FloatField(default=1)
    cena_inv = models.FloatField(default=0, blank=True)

    def __str__(self):
        return f'Inventář pro den: {self.den}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Karel INV"
        verbose_name_plural = "Karel INV"