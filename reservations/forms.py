


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

def get_default_ville():
    ville = Ville.objects.all().order_by('ordre').last()
    return ville.nom if ville else None
    
class TrajetHoraireForm(forms.Form):


    adress_depart = forms.ChoiceField(choices=get_ville_choices , widget=forms.Select(attrs={'class': 'form-select'}))
    adress_arrivee = forms.ChoiceField(choices=get_ville_choices, initial=get_default_ville  , widget=forms.Select(attrs={'class': 'form-select'}))
    date_depart = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'min': date.today().isoformat(),
        'value': date.today().isoformat()
    }))
    Nombre_place=forms.IntegerField(initial=1, min_value=1 , widget=forms.NumberInput(attrs={'class': 'form-control'}))

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenoms', 'email', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    
