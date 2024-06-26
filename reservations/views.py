from datetime import date, datetime, timedelta
import json
from django.core import serializers

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from reservations.models import Avantage, Client, Horaire, Reservation, Segment, SegmentHoraire, SegmentSegmentHoraire, Trajet, TrajetSegment, Ville
from .forms import ClientForm, TrajetHoraireForm
from django.db.models import F



# listings/views.py



def essayons(request):
        form = TrajetHoraireForm()
        
        return render(request, 'reservations/home.html', {'form': form})



# Create your views here.

def rechercher_trajet(request):
    if request.method == 'POST':
        form = TrajetHoraireForm(request.POST)

        if form.is_valid():
            adresse_depart = form.cleaned_data['adress_depart']
            adresse_arrivee = form.cleaned_data['adress_arrivee']
            date_depart = form.cleaned_data['date_depart']
            nombre_place=form.cleaned_data['Nombre_place']

            segments_disponibles = []
            

            # Recherche de l'horaire avec la date de départ spécifiée
            trajets = Trajet.objects.filter(date_depart=date_depart)
            print("Trajet disponibles:", trajets)


            for trajet in trajets:
                id_trajet=trajet.id
                trajetsegments = TrajetSegment.objects.filter(trajet_id=id_trajet)
                for  trajetsegment in trajetsegments:
                    id_segment=trajetsegment.segment_id.id

                    print("segggg", trajet.segments.all())
                    segments_seg= Segment.objects.filter(id=id_segment)
                    print("segments_seg:", segments_seg)
                    segments_disponible=segments_seg.filter(depart=adresse_depart , arrivee= adresse_arrivee)
                    print("segmentOOKOK_disponible:", segments_disponible)

                    for segment in segments_disponible:
                        print("segments_:", segments_disponibles)
                        now = datetime.now()
                        act_date = now.date()
                        time_actuel_20 = now - timedelta(minutes=20)
                        if date_depart==act_date:
                            horairesegments = segment.horairesegment.filter(heure_depart__gte=time_actuel_20)
                        else:

                            horairesegments = segment.horairesegment.all()


                        for  horairesegment in horairesegments:
                            
                            segmentsegmenthoraires=SegmentSegmentHoraire.objects.filter(segment_id=segment , segmenthoraire_id = horairesegment , place_disponible__gte = nombre_place)
                           
                            print("HORAIRFINAL",segmentsegmenthoraires)
                        
                            for  segmentsegmenthorairess in segmentsegmenthoraires:
                                print("SECSECSESmnt", segmentsegmenthorairess.segmenthoraire_id)

                                segmentsegmenthoraire=segmentsegmenthorairess 
                    
                            segments_disponibles.append((trajet, segment, horairesegments,trajetsegment, segmentsegmenthoraire , segmentsegmenthoraires))
                    if segments_disponibles :
                        request.session['key_nombre_place'] = nombre_place
                        nombre_plac = request.session.get('key_nombre_place')

                        print(f"Nombre de places défini dans la session: {nombre_place}")
                        print(f"Nombre de places défini apres dans la session: {nombre_plac}")





        
            print("Segments disponibles:", segments_disponibles)
            return render(request, 'reservations/TrajetsDisponible.html', {'segments_disponibles': segments_disponibles, 'form': form})
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

        
def Reservation_trajet(request , id_trajet , id_segment , id_segmentsegmenthoraire):
    if request.method == 'POST':
                
                # Créer une instance de formulaire et la remplir avec les données de la requête
                form = ClientForm(request.POST)
                if form.is_valid():
                    informations=[]

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
                    segmentsegmenthoraire_instance = get_object_or_404(SegmentSegmentHoraire, id=id_segmentsegmenthoraire)
                    client_instance = get_object_or_404(Client, id=client.id)


                    nombre_place = request.session.get('key_nombre_place')

                    reservation = Reservation.objects.create(
                    segmenthoraire_id=segmentsegmenthoraire_instance,
                    nombre_de_place=nombre_place,
                    client_id=client_instance,
                    # Vous pouvez générer un numéro de réservation unique ici
                    )
                    reservation.save()
                    nombre_place = request.session.get('key_nombre_place')
                    print("Nombre de place" , nombre_place)
                    trajetsegments = TrajetSegment.objects.get(trajet_id=id_trajet, segment_id=id_segment)
                    horaire = SegmentSegmentHoraire.objects.get(id=id_segmentsegmenthoraire)
                    segment = Segment.objects.get(id=id_segment)

                    trajet = Trajet.objects.get(id=id_trajet)
                    reservation = Reservation.objects.get(id=reservation.id)

                    immatriculation = trajet.car.immatriculation
                    depart=segment.depart
                    arrivee = segment.arrivee
                    type_car=trajet.car.type
                    place_reserve=reservation.nombre_de_place

                    informations.append((trajet ,segment, trajetsegments,  nombre_place, horaire,client_instance,immatriculation , type_car , depart , arrivee , reservation))


                    #Modificationplace_disponible pour un depart d'un segment liee  a un trajet
                    segsegmenthoraires = SegmentSegmentHoraire.objects.filter(segment_id=segment).order_by('id')
                    segsegmenthoraires_list = list(segsegmenthoraires)
                    segsegmenthoraire_instance = segsegmenthoraires.get(id=id_segmentsegmenthoraire)
                    position_selection = segsegmenthoraires_list.index(segsegmenthoraire_instance)
                    print("position_selection",position_selection)
                    ville_depart= Ville.objects.get(nom=depart)
                    ville_arrivee= Ville.objects.get(nom=arrivee)
                    ordre_depart=ville_depart.ordre
                    ordre_arrivee=ville_arrivee.ordre
                    segmenttrajets=TrajetSegment.objects.filter(trajet_id = trajet)
                    
                    # segmenttrajets = trajet.segments.all()
                    print("ordre_depart", ordre_depart)
                    print("ordre_arrivee", ordre_arrivee)

                    print("SEGMENTVERIFIER" , segmenttrajets)
                    for segmenttrajet in segmenttrajets:
                        depart=segmenttrajet.segment_id.depart
                        segment_id=segmenttrajet.segment_id
                        print("deopart" , depart)
                        villedepart_seg= Ville.objects.get(nom=depart)
                        ordredepart_seg = villedepart_seg.ordre
                        print("ordredepart_seg" , ordredepart_seg)

                        if  ordre_depart==ordredepart_seg:
                            print("PremierBien jouer")
                            print("Premierhoraire.segmenthoraire_id" , horaire.segmenthoraire_id)
                            # segmenthoraireH= SegmentSegmentHoraire.objects.filter(segment_id=segment_id)
                            # depart_seghoraire= segmenthoraireH.segmenthoraire_id.heure_depart.all()
                        

                            segmenthoraireH= SegmentSegmentHoraire.objects.filter(segment_id=segment_id , segmenthoraire_id__heure_depart= horaire.segmenthoraire_id.heure_depart)


                            segmenthoraire= SegmentSegmentHoraire.objects.filter(segment_id=segment_id , segmenthoraire_id__heure_depart= horaire.segmenthoraire_id.heure_depart).update(place_disponible =F('place_disponible') - place_reserve)
                            print("Segmenthoraire :" , segmenthoraireH)
                            print("Bien enregistrer")
                            # print("Debut elif")
                        if (ordre_arrivee - ordre_depart) > 0:
                            if((ordredepart_seg > ordre_depart) and (ordredepart_seg < ordre_arrivee)):

                                print("Ordre supperieur")

                                segmenthoraires = SegmentSegmentHoraire.objects.filter(segment_id=segment_id)
                                print("super")
                                segmenthoraires_list = list(segmenthoraires)
                                print("Bien")

                                segmenthoraires = segmenthoraires_list[position_selection]
                                print("ordreSupp",segmenthoraires)
                                print("segmentid_horaire:", segmenthoraires.segmenthoraire_id)
                                segmenthoraire= SegmentSegmentHoraire.objects.filter(segment_id=segment_id ,  id= segmenthoraires.id).update(place_disponible =F('place_disponible') - place_reserve)

                                # # segmenthorainstance=SegmentHoraire.objects.get(id=segment_id )
                                # print("place_disponible:", segmenthoraires.place_disponible)
                                # print("segment_id:", segmenthoraires.segment_id)


                                # segmenthoraires.place_disponible -= place_reserve

                                # try:
                                #     segmenthoraires.save(update_fields=['place_disponible'])
                                #     print("place_disponible après modification:", segmenthoraires.place_disponible)
                                #     print("DeuxiemeBien jouer")
                                # except Exception as e:
                                #     print("Erreur lors de la sauvegarde:", e)
                                
                        else:
                            if ((ordredepart_seg < ordre_depart) and (ordredepart_seg > ordre_arrivee)):
                                print("Ordre Inferieur")

                                segmenthoraires = SegmentSegmentHoraire.objects.filter(segment_id=segment_id)
                                print("super")
                                segmenthoraires_list = list(segmenthoraires)
                                print("Bien")

                                segmenthoraires = segmenthoraires_list[position_selection]
                                print("ordreinf",segmenthoraires)
                                print("ordreInf",segmenthoraire)
                                print("segmentid_horaire:", segmenthoraires.id)
                                print("place_disponible:", segmenthoraires.place_disponible)
                                print("segment_id:", segmenthoraires.segment_id)
                                segmenthoraire= SegmentSegmentHoraire.objects.filter(segment_id=segment_id , id= segmenthoraires.id).update(place_disponible =F('place_disponible') - place_reserve)


                                # segmenthoraires.place_disponible -= place_reserve
                                # try:
                                #     segmenthoraires.save(update_fields=['place_disponible'])
                                #     print("place_disponible après modification:", segmenthoraires.place_disponible)
                                #     print("DeuxiemeBien jouer")
                                # except Exception as e:
                                #     print("Erreur lors de la sauvegarde:", e)
                                # print("TroixiemeBien jouer")

                    if informations:
                        print("reservationsuccees" ,informations)

                        # print("reservationsuccees")
                        return render(request, 'reservations/TravelTicket.html', {'informations': informations})
                    else:
                        return render(request, 'reservations/ReservationTicket.html', {'form': form})


                    # return redirect('ticket', id_trajet=id_trajet, id_segment=id_segment, id_segmentsegmenthoraire=id_segmentsegmenthoraire)
                    
                else:
                    form = ClientForm()
    else:
        form = ClientForm()
    return render(request, 'reservations/ReservationTicket.html', {'form': form})

# def Travel_tiket(request , id_trajet , id_segment , id_segmentsegmenthoraire):
        
#         if request.method == 'POST':
#         # Créer une instance de formulaire et la remplir avec les données de la requête
#             form = ClientForm(request.POST)
#             if form.is_valid():
#             # Enregistrer le client dans la base de données
#                 prenoms = form.cleaned_data['prenoms']
#                 email = form.cleaned_data['email']
#                 telephone = form.cleaned_data['telephone']
#                 nom = form.cleaned_data['nom']
#                 client = Client.objects.create(
#                     nom=nom,
#                     prenoms=prenoms,
#                     email=email,
#                     telephone=telephone,
#                 )
#                 client.save()

#                 reservation = Reservation.objects.create(
#                 segmenthoraire_id=id_segmentsegmenthoraire,
#                 nombre_de_place=id_segment,
#                 client_id=client.id,
#                 # Vous pouvez générer un numéro de réservation unique ici
#                 )
#                 reservation.save()
#             # Rediriger l'utilisateur vers une autre page après l'enregistrement
#                 #return redirect('page_de_confirmation')
#         else:
#             # Si la requête est GET, afficher un formulaire vide
#             form = ClientForm()



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

def Ticket(request , id_trajet , id_segment , id_segmentsegmenthoraire ):  
    return render(request, 'reservations/TravelTicket.html')

