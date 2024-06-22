# Generated by Django 5.0.6 on 2024-06-22 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_remove_trajet_prix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trajet',
            name='segments',
            field=models.ManyToManyField(blank=True, related_name='Trajet', to='reservations.segment'),
        ),
    ]
