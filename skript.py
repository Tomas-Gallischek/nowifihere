import os
import django
import numpy as np # Pro generování hodnot s plovoucí desetinnou čárkou

# Nastavení Django prostředí
# Nahraďte 'your_project_name' skutečným názvem vašeho projektu
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NOWIFI.settings')
django.setup()

# Nahraďte 'your_app_name' skutečným názvem vaší aplikace, kde je model definován
from adminapp.models import aktivita_kcal2

# Konstanty pro modelového muže
WEIGHT_KG = 85  # Váha v kg

# Konstanty pro mapování tempa na METs
# METs = (A_CONST * tempo + B_CONST) / C_CONST
# A_CONST = 18.8, B_CONST = 22, C_CONST = 19.9
# Nebo přesněji: METs = METS_SLOPE * tempo + METS_INTERCEPT
METS_SLOPE = 18.8 / 19.9
METS_INTERCEPT = 22 / 19.9 # Ekvivalent (1.2 * 19.9 - 18.8 * 0.1) / 19.9

def calculate_kcal_for_tempo(tempo_value):
    """
    Vypočítá odhadované spálené kalorie za hodinu pro dané tempo.
    """
    # Mapování 'tempo' (0.1 až 20) na METs (1.2 až 20)
    mapped_mets = METS_SLOPE * tempo_value + METS_INTERCEPT
    
    # Výpočet kalorií za hodinu: METs * váha (kg)
    kcal_per_hour = (mapped_mets * WEIGHT_KG)*0.7
    
    return int(round(kcal_per_hour))

def populate_database():
    """
    Naplní databázi 'aktivita_kcal2' hodnotami tempa a odhadovanými kaloriemi.
    """
    print("Startuji plnění databáze...")

    # Generování hodnot tempa od 0.1 do 20.0 s krokem 0.1
    # Použijeme np.linspace pro zajištění přesného počtu 200 bodů včetně koncových.
    tempo_values = np.linspace(0.1, 20.0, num=200)

    records_created_count = 0
    for tempo_raw in tempo_values:
        # Zaokrouhlení na jedno desetinné místo pro konzistenci
        tempo = round(tempo_raw, 1)
        
        kcal = calculate_kcal_for_tempo(tempo)
        
        try:
            aktivita_kcal2.objects.create(
                tempo=tempo,
                kcal_za_hodinu=kcal
            )
            # print(f"Vytvořen záznam: Tempo {tempo:.1f}, Kcal/h {kcal}")
            records_created_count += 1
        except Exception as e:
            print(f"Chyba při vytváření záznamu pro tempo {tempo:.1f}: {e}")

    print(f"Plnění databáze dokončeno. Bylo vytvořeno {records_created_count} záznamů.")
    expected_records = len(tempo_values)
    if records_created_count == expected_records:
        print(f"Očekávaný počet záznamů ({expected_records}) byl úspěšně přidán.")
    else:
        print(f"Varování: Očekávalo se {expected_records} záznamů, ale bylo přidáno {records_created_count}.")


if __name__ == '__main__':
    # Pokud byste chtěli před každým spuštěním smazat existující data (buďte opatrní!):
    # print("Mažu existující data z tabulky aktivita_kcal2...")
    # aktivita_kcal2.objects.all().delete()
    # print("Existující data smazána.")
    
    populate_database()

    # Příklad výpočtu pro ověření:
    # print(f"\nTestovací výpočty:")
    # print(f"Tempo 0.1: METs = {round(METS_SLOPE * 0.1 + METS_INTERCEPT, 2)}, Kcal/h = {calculate_kcal_for_tempo(0.1)}")
    # print(f"Tempo 1.0: METs = {round(METS_SLOPE * 1.0 + METS_INTERCEPT, 2)}, Kcal/h = {calculate_kcal_for_tempo(1.0)}")
    # print(f"Tempo 10.0: METs = {round(METS_SLOPE * 10.0 + METS_INTERCEPT, 2)}, Kcal/h = {calculate_kcal_for_tempo(10.0)}")
    # print(f"Tempo 20.0: METs = {round(METS_SLOPE * 20.0 + METS_INTERCEPT, 2)}, Kcal/h = {calculate_kcal_for_tempo(20.0)}")