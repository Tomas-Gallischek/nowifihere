# Generated by Django 5.1.5 on 2025-05-30 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infopage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vysledky_hracu',
            name='prijmeni',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
