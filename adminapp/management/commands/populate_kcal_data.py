from django.core.management.base import BaseCommand
from adminapp.models import aktivita_kcal2  # Nahraďte 'app_vaseho_projektu' názvem vaší aplikace

class Command(BaseCommand):
    help = 'Automaticky vyplní tabulku aktivita_kcal2 daty pro chůzi'

    def handle(self, *args, **options):
        # Smazání stávajících dat
        aktivita_kcal2.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Stávající data byla smazána.'))

        vaha_kg = 85
        met_na_kmh = {
            3: 2.0,   # Velmi pomalá chůze
            4: 2.8,   # Pomala chůze
            5: 3.5,   # Průměrná chůze
            6: 4.3,   # Rychlá chůze
            7: 5.0,   # Velmi rychlá chůze
        }

        for tempo_kmh in [round(i * 0.1, 1) for i in range(1, 201)]:
            # Převod tempa z km/h na m/min (pro lepší odhad MET) - toto je spíše pro přesnější mapování, nemusí být nutné
            tempo_ms = tempo_kmh * 1000 / 3600
            tempo_mmin = tempo_ms * 60

            # Zjednodušený odhad MET na základě tempa (lze vylepšit s detailnější mapou)
            if tempo_kmh < 3:
                met = met_na_kmh.get(3, 2.0)
            elif 3 <= tempo_kmh < 4:
                met = met_na_kmh.get(4, 2.8)
            elif 4 <= tempo_kmh < 5:
                met = met_na_kmh.get(5, 3.5)
            elif 5 <= tempo_kmh < 6:
                met = met_na_kmh.get(6, 4.3)
            elif 6 <= tempo_kmh:
                met = met_na_kmh.get(7, 5.0)
            else:
                met = 2.0

            # Vzorec pro výpočet kalorií za hodinu: MET x 3.5 x váha (kg) / 200 * 60
            kcal_za_hodinu = int(met * 1 * vaha_kg)

            aktivita = aktivita_kcal2(tempo=tempo_kmh, kcal_za_hodinu=kcal_za_hodinu)
            aktivita.save()

        self.stdout.write(self.style.SUCCESS('Data pro aktivity byla úspěšně vložena.'))