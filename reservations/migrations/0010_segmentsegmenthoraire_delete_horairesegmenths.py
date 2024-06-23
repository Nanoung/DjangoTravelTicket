# Generated by Django 5.0.6 on 2024-06-23 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0009_horairesegmenths_delete_horairesegment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SegmentSegmentHoraire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_disponible', models.IntegerField(default=0)),
                ('segment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.segment')),
                ('segmenthoraire_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.segmenthoraire')),
            ],
        ),
        migrations.DeleteModel(
            name='HoraireSegmentHS',
        ),
    ]
