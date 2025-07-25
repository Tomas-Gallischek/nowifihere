# Generated by Django 5.1.5 on 2025-05-26 07:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='aktivita_kcal2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tempo', models.FloatField()),
                ('kcal_za_hodinu', models.IntegerField()),
            ],
            options={
                'verbose_name': 'vÝPOČET kcal/h',
                'verbose_name_plural': 'vÝPOČET kcal/h',
            },
        ),
        migrations.CreateModel(
            name='aktualniden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cislo_dne', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(12)])),
            ],
            options={
                'verbose_name': 'Přepnout den',
                'verbose_name_plural': 'Přepnout den',
            },
        ),
        migrations.CreateModel(
            name='food_drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_img', models.ImageField(blank=True, upload_to='food_images/')),
                ('food_name', models.CharField(max_length=1000)),
                ('food_znacka', models.CharField(max_length=1000)),
                ('food_typ', models.CharField(max_length=1000)),
                ('food_vaha', models.FloatField(default=0, max_length=1000)),
                ('food_objem', models.FloatField(default=0, max_length=1000)),
                ('food_kcal', models.FloatField(default=0, max_length=1000)),
                ('food_sytost', models.FloatField(default=0, max_length=1000)),
                ('food_hydratace', models.FloatField(default=0, max_length=1000)),
                ('food_cena', models.FloatField(default=0, max_length=1000)),
            ],
            options={
                'verbose_name': 'Databáze: Jídlo + pití',
                'verbose_name_plural': 'Databáze: Jídlo + pití',
            },
        ),
        migrations.CreateModel(
            name='hraci_v_tymu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pocet_hracu_pepa', models.IntegerField(blank=True, default=0)),
                ('pocet_hracu_karel', models.IntegerField(blank=True, default=0)),
                ('pocet_hracu_brunhilda', models.IntegerField(blank=True, default=0)),
                ('hraci_celkem', models.IntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'Počet hráčů v týmech',
                'verbose_name_plural': 'Počet hráčů v týmech',
            },
        ),
        migrations.CreateModel(
            name='hubnuti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rozdil_kcal', models.IntegerField()),
                ('kg_rozdil_hubnuti', models.FloatField()),
            ],
            options={
                'verbose_name': 'Hubnutí',
                'verbose_name_plural': 'Hubnutí',
            },
        ),
        migrations.CreateModel(
            name='kondice_hubnuti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hubnuti', models.FloatField()),
                ('hubnuti_kondice', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Hubnutí - kondice',
                'verbose_name_plural': 'Hubnutí - kondice',
            },
        ),
        migrations.CreateModel(
            name='motivacni_citat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citat', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='pamet_pepa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('den', models.IntegerField(blank=True)),
                ('energie', models.IntegerField(blank=True)),
                ('kondice', models.IntegerField(blank=True)),
                ('hydratace', models.IntegerField(blank=True)),
                ('sytost', models.IntegerField(blank=True)),
                ('zatez', models.IntegerField(blank=True)),
                ('volna_kapacita', models.FloatField(blank=True)),
                ('pepova_aktualni_vaha', models.FloatField(blank=True, default=0)),
                ('zustatek_na_ucte', models.FloatField(blank=True, default=0)),
                ('km_s_bonusem', models.FloatField(blank=True, default=0)),
                ('aktual_XP', models.IntegerField(blank=True, default=0)),
                ('pozn', models.CharField(blank=True, max_length=1000)),
            ],
            options={
                'verbose_name': 'Paměť - PEPA',
                'verbose_name_plural': 'Paměť - PEPA',
            },
        ),
        migrations.CreateModel(
            name='spanek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('den', models.IntegerField()),
                ('pepa_spanek', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(12)])),
                ('karel_spanek', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(12)])),
                ('brunhilda_spanek', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(12)])),
                ('pepa_aktivita', models.IntegerField(default=0)),
                ('karel_aktivita', models.IntegerField(default=0)),
                ('brunhilda_aktivita', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Kolik kdo spal',
                'verbose_name_plural': 'Kolik kdo spal',
            },
        ),
        migrations.CreateModel(
            name='vybava',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_img', models.ImageField(blank=True, upload_to='item_images/')),
                ('item_name', models.CharField(max_length=1000)),
                ('item_znacka', models.CharField(max_length=1000)),
                ('item_typ', models.CharField(max_length=1000)),
                ('item_vaha', models.FloatField(default=0, max_length=1000)),
                ('item_objem', models.FloatField(default=0, max_length=1000)),
                ('item_bonus_delka_kroku_procenta', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_BMR_procenta', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_zatez_procenta', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_income_FLAT', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_income_procenta', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_kapacita_FLAT', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_kapacita_procenta', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_XP_procenta', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_XP_FLAT', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_spanek_FLAT', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_spanek_procenta', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_bonus_cena_procenta', models.FloatField(blank=True, default=0, max_length=1000)),
                ('item_cena', models.FloatField(default=0, max_length=1000)),
                ('item_pozn', models.CharField(default=models.CharField(max_length=1000), max_length=1000)),
            ],
            options={
                'verbose_name': 'Databáze: Výbava',
                'verbose_name_plural': 'Databáze: Výbava',
            },
        ),
    ]
