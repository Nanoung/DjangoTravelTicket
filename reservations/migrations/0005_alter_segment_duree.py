# Generated by Django 5.0.6 on 2024-06-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_trajet_prix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='duree',
            field=models.IntegerField(help_text='Durée en minutes', null=True),
        ),
    ]
