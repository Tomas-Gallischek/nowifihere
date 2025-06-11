from django.db import models
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from numpy import True_, true_divide

class vysledky_hracu(models.Model):
    jmeno = models.CharField(max_length=20)
    prijmeni = models.CharField(max_length=30, blank=True)
    tym = models.CharField(max_length=10, null=True)
    # Odstraněn max_length u FloatField, není standardní
    koeficient = models.FloatField(null=True, blank=True, default=1)
    kroky_BONUS = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky1 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky2 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky3 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky4 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky5 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky6 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky7 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky8 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky9 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky10 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky11 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    kroky12 = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    max_kroku_mesicne = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    celkem_kroku = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1000000)])


    # formát zobrazení v administraci
    def __str__(self):
        return f'{self.jmeno} {self.prijmeni}'
    
    def save(self, *args, **kwargs):
        # Výpočet celkového počtu kroků (z hodnot PŘED aplikací koeficientu na měsíční kroky)
        self.celkem_kroku = (
            (self.kroky1 or 0) + (self.kroky2 or 0) + (self.kroky3 or 0) + (self.kroky4 or 0) +
            (self.kroky5 or 0) + (self.kroky6 or 0) + (self.kroky7 or 0) + (self.kroky8 or 0) +
            (self.kroky9 or 0) + (self.kroky10 or 0) + (self.kroky11 or 0) + (self.kroky12 or 0) +
            (self.kroky_BONUS or 0)
        )

        koeficient = self.koeficient if self.koeficient is not None else 1

        # Aplikace koeficientu na jednotlivé měsíční kroky
        self.kroky1 = int(round((self.kroky1 or 0) * koeficient))
        self.kroky2 = int(round((self.kroky2 or 0) * koeficient))
        self.kroky3 = int(round((self.kroky3 or 0) * koeficient))
        self.kroky4 = int(round((self.kroky4 or 0) * koeficient))
        self.kroky5 = int(round((self.kroky5 or 0) * koeficient))
        self.kroky6 = int(round((self.kroky6 or 0) * koeficient))
        self.kroky7 = int(round((self.kroky7 or 0) * koeficient))
        self.kroky8 = int(round((self.kroky8 or 0) * koeficient))
        self.kroky9 = int(round((self.kroky9 or 0) * koeficient))
        self.kroky10 = int(round((self.kroky10 or 0) * koeficient))
        self.kroky11 = int(round((self.kroky11 or 0) * koeficient))
        self.kroky12 = int(round((self.kroky12 or 0) * koeficient))

        # Výpočet nejvyšší hodnoty z kroky1 až kroky12 (již po aplikaci koeficientu)
        kroky_po_koeficientu = [
            self.kroky1, self.kroky2, self.kroky3, self.kroky4,
            self.kroky5, self.kroky6, self.kroky7, self.kroky8,
            self.kroky9, self.kroky10, self.kroky11, self.kroky12
        ]
        self.max_kroku_mesicne = max(kroky_po_koeficientu)
        
        super().save(*args, **kwargs) # Volání původní metody save()

    class Meta:
        verbose_name = "Výsledky hráčů"
        verbose_name_plural = "Výsledky hráčů"