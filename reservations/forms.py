


from datetime import date
from django import forms

from reservations.models import Client, Horaire, Trajet

"""
class TrajetForm(forms.ModelForm):
    class Meta:
        model = Trajet
        model = Horaire
        fields = ['adress_depart', 'adress_arrivee', 'date_depart']
        widgets ={
            'date_depart': forms.DateInput(attrs={
                'type': 'date',
                'min': date.today().isoformat(),
                'value': date.today().isoformat()

            }
            ),
        }
"""


class TrajetHoraireForm(forms.Form):

    Ville = [
    ('Korhogo', 'Korhogo'),
    ('Bouaké', 'Bouaké'),
    ('Yamoussoukro', 'Yamoussoukro'),
    ('Abidjan', 'Abidjan'),
]

    adress_depart = forms.ChoiceField(choices=Ville)
    adress_arrivee = forms.ChoiceField(choices=Ville)
    date_depart = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'min': date.today().isoformat(),
        'value': date.today().isoformat()
    }))
    Nombre_place=forms.IntegerField(initial=1, min_value=1)

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenoms', 'email', 'telephone']