from datetime import date
from django.shortcuts import redirect, render

from reservations.models import Horaire, Segment, Trajet
from .forms import TrajetHoraireForm


# listings/views.py



def essayons(request):
        form = TrajetHoraireForm()
        
        return render(request, 'reservations/home.html', {'form': form})



# Create your views here.

def rechercher_trajet(request):
    
    today = date.today().isoformat()
    trajets = None
    segments =None
    horaires = None

    segments_disponibles = []

    if request.method == 'POST':
        form = TrajetHoraireForm(request.POST)

        if form.is_valid():
            adresse_depart = form.cleaned_data['adress_depart']
            adresse_arrivee = form.cleaned_data['adress_arrivee']
            date_depart = form.cleaned_data['date_depart']
            # Recherche de l'horaire avec la date de départ spécifiée
            trajets = Trajet.objects.filter(date_depart=date_depart)
            for trajet in trajets:
                #for horaire in trajet.horaires.all():
                    #if horaire.heure_depart.date() == date_depart:
                segments_filtres=trajet.segments.filter(depart=adresse_depart, arrivee=adresse_arrivee)
                for segment in segments_filtres:
                    horairesegments = segment.horairesegment.all()  # Utilisation correcte sans les parenthèses
                    segments_disponibles.append((trajet, segment, horairesegments))
                            #segments_disponibles = trajet.segments.filter(depart=adresse_depart, arrivee=adresse_arrivee)
                        #trajets_disponibles.append((trajet, horaire, segments_filtrés))

            return render(request, 'reservations/TrajetsDisponible.html', {'segments_disponibles': segments_disponibles})
    else:
        form = TrajetHoraireForm()
    return render(request, 'reservations/home.html', {'form': form})