from datetime import date
from django.shortcuts import redirect, render

from reservations.models import Horaire, Segment, Trajet
from .forms import TrajetHoraireForm


# listings/views.py



def essayons(request):
    return render(request, 'reservations/home.html')


# Create your views here.

def rechercher_trajet(request):
    
    today = date.today().isoformat()
    trajets = None
    segments =None
    horaires = None

    
    if request.method == 'POST':
            form = TrajetHoraireForm(request.POST)

            if form.is_valid():
                adresse_depart = form.cleaned_data['adresse_depart']
            adresse_arrivee = form.cleaned_data['adresse_arrivee']
            date_depart = form.cleaned_data['date_depart']
            # Recherche de l'horaire avec la date de départ spécifiée
            horaire = Horaire.objects.get(date_depart=date_depart)
            # Récupération du trajet associé à cet horaire
            trajets = Trajet.objects.get(horaires=horaire)
            # Récupération de tous les segments associés à ce trajet
            segments = trajets.segments.all()
            # Filtrer les segments en fonction des adresses de départ et d'arrivée spécifiées
            segments_disponibles = segments.filter(depart=adresse_depart, arrivee=adresse_arrivee)
            return render(request, 'TrajetsDisponible.html', {'segments_disponibles': segments_disponibles})
    else:
        form = TrajetHoraireForm()
    return render(request, 'votre_formulaire_template.html', {'form': form})