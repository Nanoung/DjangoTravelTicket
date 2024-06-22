


from datetime import date
from django import forms

from reservations.models import Client, Horaire, Trajet, Ville

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

def get_ville_choices():
        villes = Ville.objects.all().order_by('ordre')
        return [(ville.nom, ville.nom) for ville in villes]
    
class TrajetHoraireForm(forms.Form):


    adress_depart = forms.ChoiceField(choices=get_ville_choices)
    adress_arrivee = forms.ChoiceField(choices=get_ville_choices)
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

    
