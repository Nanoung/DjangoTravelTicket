# Generated by Django 5.0.6 on 2024-06-11 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_alter_segment_duree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='duree',
            field=models.IntegerField(default=480, help_text='Durée en minutes'),
        ),
    ]