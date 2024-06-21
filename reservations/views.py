from datetime import date
import json
from django.core import serializers

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from reservations.models import Avantage, Client, Horaire, Reservation, Segment, SegmentHoraire, Trajet, TrajetSegment
from .forms import ClientForm, TrajetHoraireForm


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
            nombre_place = form.cleaned_data['Nombre_place']
            # request.session['Nombre_place'] = nombre_place



            # Recherche de l'horaire avec la date de départ spécifiée
            trajets = Trajet.objects.filter(date_depart=date_depart)

            for trajet in trajets:
                #for horaire in trajet.horaires.all():
                    #if horaire.heure_depart.date() == date_depart:
                segments_filtres=trajet.segments.filter(depart=adresse_depart, arrivee=adresse_arrivee , )

                for segment in segments_filtres:
                    trajet_segments = TrajetSegment.objects.filter(segment_id=segment.id , trajet_id = trajet.id , place_disponible__gte=nombre_place)
                    for trajet_segment in trajet_segments:
                       # prix=trajet_segment.prix_segment
                         
                

                        horairesegments = segment.horairesegment.all() 
                          # Utilisation correcte sans les parenthèses
                        segments_disponibles.append((trajet, segment, horairesegments,trajet_segment))
                                #segments_disponibles = trajet.segments.filter(depart=adresse_depart, arrivee=adresse_arrivee)
                        #trajets_disponibles.append((trajet, horaire, segments_filtrés))

            return render(request, 'reservations/TrajetsDisponible.html', {'segments_disponibles': segments_disponibles ,
                                                                           'form': form
                                                                           })
    else:
        form = TrajetHoraireForm()
    return render(request, 'reservations/home.html', {'form': form})

def details_trajet(request, id_trajet , id_segment , id_horaire):
        #trajet = get_object_or_404(Trajet, id=id_trajet)
        #segment = get_object_or_404(Segment, id_=id)
    try:
        trajet = Trajet.objects.get(id=id_trajet)
        segment = get_object_or_404(Segment, id=id_segment)
        trajet_segments = TrajetSegment.objects.get(segment_id=id_segment , trajet_id = id_trajet)
        avantages = trajet.car.type.avantages
        horaire=SegmentHoraire.objects.get(id=id_horaire)

    


        trajets={
             
             "arrivee":segment.arrivee,
             'id':trajet.id,
             "depart" : segment.depart,
             "id_segment" : segment.id,
             "prix" : trajet_segments.prix_segment,
              "car" : trajet.car.immatriculation,
              "type" : trajet.car.type.nom,
              "heure_depart":horaire.heure_depart,  
            "heure_arrivee":horaire.heure_arrivee,
            "id_horaire" : horaire.id,

             "avantages": list(avantages.values('id', 'nom', 'description'))
        }
        try:
            trajets["car"] = trajet.car.immatriculation
        except AttributeError:
            trajets["car"] = "Immatriculation indisponible"

        # trajet_json = serializers.serialize('json', [trajets])
        # trajet_data = json.loads(trajet_json)
        return JsonResponse({'trajet': trajets})
    except Trajet.DoesNotExist:
        return JsonResponse({'error': 'Trajet non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        
def Reservation_trajet(request , id_trajet , id_segment , id_horaire):
        form = ClientForm()
        
        id_trajets=id_trajet
        id_segments=id_segment
        id_horaires=id_horaire
        urlelement={
            'form': form,
            "id_trajets":id_trajets,
            "id_segments":id_segments,
            "id_horaires":id_horaires
             
        }
        return render(request, 'reservations/ReservationTicket.html', {"urlelement":urlelement})

def Travel_tiket(request , id_trajet , id_segment , id_horaire):
        
        if request.method == 'POST':
        # Créer une instance de formulaire et la remplir avec les données de la requête
            form = ClientForm(request.POST)
            if form.is_valid():
            # Enregistrer le client dans la base de données
                prenoms = form.cleaned_data['prenoms']
                email = form.cleaned_data['email']
                telephone = form.cleaned_data['telephone']
                nom = form.cleaned_data['nom']
                client = Client.objects.create(
                    nom=nom,
                    prenoms=prenoms,
                    email=email,
                    telephone=telephone,
                )
                client.save()

                reservation = Reservation.objects.create(
                trajet_id=id_trajet,
                segment_id=id_segment,
                client_id=client.id,
                # Vous pouvez générer un numéro de réservation unique ici
                )
                reservation.save()
            # Rediriger l'utilisateur vers une autre page après l'enregistrement
                #return redirect('page_de_confirmation')
        else:
            # Si la requête est GET, afficher un formulaire vide
            form = ClientForm()



        # try:
        #     # forms = TrajetHoraireForm(request.POST)



        #     #client=Client.objeect
        #     trajet = Trajet.objects.get(id=id_trajet)
        #     segment = get_object_or_404(Segment, id=id_segment)
        #     trajet_segments = TrajetSegment.objects.get(segment_id=id_segment , trajet_id = id_trajet)
        #     avantages = trajet.car.type.avantages
        #     horaire=SegmentHoraire.objects.get(id=id_horaire)
        #     nombre_place = request.session.get('nombre_place')            # nom=forms.cleaned_data['nom']
        #     # prenoms=forms.cleaned_data['prenoms']
        #     # email=forms.cleaned_data['email']
        #     # telephone=forms.cleaned_data['telephone']






    


        #     trajets={
                
        #         "arrivee":segment.arrivee,
        #         'id':trajet.id,
        #         "depart" : segment.depart,
        #         "id_segment" : segment.id,
        #         "prix" : trajet_segments.prix_segment,
        #         "car" : trajet.car.immatriculation,
        #         "type" : trajet.car.type.nom,
        #         "heure_depart":horaire.heure_depart,  
        #         "heure_arrivee":horaire.heure_arrivee,
        #         "id_horaire" : horaire.id,
        #          "nombre_place" : nombre_place,
        #         # "nom" : nom,
        #         # "prenoms": prenoms,
        #         # "email" : email,
        #         # "telephone" :telephone,

        #         "avantages": list(avantages.values('id', 'nom', 'description'))
        #     }
            

        # # trajet_json = serializers.serialize('json', [trajets])
        # # trajet_data = json.loads(trajet_json)
        #     return JsonResponse({'trajet': trajets})
        # except Trajet.DoesNotExist:
        #     return JsonResponse({'error': 'Trajet non trouvé'}, status=404)
        # # except Exception as e:
        #     return JsonResponse({'error': str(e)}, status=500)


