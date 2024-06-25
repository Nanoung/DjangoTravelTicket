from datetime import *
from decimal import Decimal
from itertools import combinations
import logging

from django.utils import timezone
#from datetime import date, datetime, timedelta, timezone
import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.db import transaction
from django.db.models import Q




# Create your models here.

# class Ville(models.TextChoices):
#         Korhogo = 'Korhogo'
#         Bouaké = 'Bouaké'
#         Yamoussoukro = 'Yamoussoukro'
#         Abidjan = 'Abidjan'
class Ville(models.Model):
        nom=models.CharField(max_length=100)
        ordre=models.IntegerField(editable=False, unique=True)
        def __str__(self):
            return f"{self.nom}"

@receiver(pre_save, sender=Ville)
def set_ville_ordre(sender, instance, **kwargs):
    if not instance.pk:
        max_ordre = Ville.objects.all().aggregate(models.Max('ordre'))['ordre__max']
        instance.ordre = 1 if max_ordre is None else max_ordre + 1
        
        

class Avantage(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f" {self.nom}"
    


class Type(models.TextChoices):
        standard = 'Standard'
        premium = 'Premium'
        

class CarType(models.Model):
    nom = models.CharField(choices=Type.choices, max_length=100)
    avantages = models.ManyToManyField(Avantage, related_name='car_types')

    def __str__(self):
        return f" {self.nom}"
    

class Cars(models.Model):

    immatriculation = models.CharField(max_length=100)
    nombre_places = models.IntegerField()
    type = models.ForeignKey(CarType, on_delete=models.CASCADE, related_name='cars')
# Cela permet d'accéder à toutes les voitures d'un type de voiture spécifique en utilisant car_type.cars.all()
    def __str__(self):
        return f" {self.immatriculation} -{self.type} "
def get_ville_choices():
        villes = Ville.objects.all().order_by('ordre')
        return [(ville.nom, ville.nom) for ville in villes]
    
class Trajet(models.Model):

    class Type(models.TextChoices):
        VIP='Vip'
        Ordinaire='Ordinaire'

    
    date_str = '2024-01-01'


# Convertir la chaîne de caractères en objet datetime
    #date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

# Utiliser l'objet datetime comme valeur par défaut pour le champ date_depart
    #date_depart = models.DateField(default=date_obj)

    date_depart= models.DateField(default=timezone.now)
    adress_depart=models.CharField(choices=get_ville_choices, max_length=50)
    adress_arrivee=models.CharField(choices=get_ville_choices,  max_length=50)
    arrets = models.ManyToManyField('Arret', related_name='Trajet',blank=True )

    nom_voyage=models.CharField(max_length=100 , blank=True)
    horaires = models.ManyToManyField('Horaire',related_name='Trajet')
    segments = models.ManyToManyField('Segment', related_name='Trajet' , blank=True)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='Trajet' , null=True)  # Relation one-to-many


    def save(self, *args, **kwargs):
        if self.adress_depart and self.adress_arrivee:
            self.nom_voyage = f"{self.adress_depart}_{self.adress_arrivee}"
        super(Trajet, self).save(*args, **kwargs)
        

    def create_segments(self):
            @receiver(m2m_changed, sender=Trajet.arrets.through)
            def arrets_changed(sender, instance, action, **kwargs):
                if action == 'post_add':
                    # Votre logique ici une fois que les arrêts ont été associés au trajet
                    arrets = instance.arrets.all()
        # Utilisez les arrêts associés au trajet  
            # self.segments.clear()      
                    # arrets = self.arrets.all() 
                    print("arrets",arrets)
                    Ville_depart = Ville.objects.get(nom=self.adress_depart)
                    Ville_arrivee = Ville.objects.get(nom=self.adress_arrivee)

                    depart_ordre = Ville_depart.ordre
                    arrivee_ordre = Ville_arrivee.ordre

                    if (depart_ordre - arrivee_ordre) > 0:
                            arrets_ordonnee=arrets.order_by('-ville__ordre')
                    else:
                            arrets_ordonnee=arrets.order_by('ville__ordre')
                    liste=[self.adress_depart]
                    for arret in arrets_ordonnee:
                            liste.append(arret)
                    liste.append(self.adress_arrivee)
                    print(liste)
                    for depart_list, arrivee_list in combinations(liste, 2):
                            
                            prix_segment=Prix_segment.objects.get(
                                (Q(depart=depart_list, arrivee=arrivee_list) | Q(depart=arrivee_list, arrivee=depart_list))
                            )
                            print("prix_segment",prix_segment)
                            trajet_segment= Segment.objects.create(
                            depart=depart_list, 
                            arrivee=arrivee_list, 
                            prix=prix_segment.prix,
                            duree=prix_segment.duree
                            )
                            try:
                                self.segments.add(trajet_segment)
                                print("ajout du segment : ")

                            except Exception as e:
                                print("Erreur lors de l'ajout du segment : ")
                    
# @receiver(m2m_changed, sender=Trajet.segments.through)
# def m2m_changed_trajet(sender, instance, action, reverse, model, pk_set, **kwargs):
#     if action == "post_add" or action == "post_clear":
#         instance.create_segments()

# @receiver(m2m_changed, sender=Trajet.arrets.through)
# def m2m_changed_arrets(sender, instance, action, reverse, model, pk_set, **kwargs):
#     if action == "post_add":
#         instance.create_segments()



@receiver(post_save, sender=Trajet)
def post_save_trajet(sender, instance, created, **kwargs):
        instance.create_segments()

class Arret(models.Model):
    ville = models.OneToOneField(Ville, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.ville.nom}"


class Horaire(models.Model):
    heure_depart = models.TimeField()
    #trajet = models.ManyToManyField('Trajet',related_name='horaire')
    def __str__(self):
       
        return f"{self.heure_depart}"




class Segment(models.Model):
    depart = models.CharField(max_length=50)
    arrivee = models.CharField(max_length=50)
    #ordre = models.IntegerField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    duree = models.IntegerField(help_text="Durée en minutes")
    horairesegment = models.ManyToManyField('SegmentHoraire',related_name='segments', blank=True)

    def __str__(self):
        horaires = self.horairesegment.all()  # Récupère tous les SegmentHoraire associés
        horaires_str = ", ".join([str(horaire) for horaire in horaires])
        return f" {self.depart} -> {self.arrivee} | Horaires: {horaires_str}"
    
class SegmentHoraire(models.Model):
    heure_depart = models.TimeField()
    heure_arrivee = models.TimeField(null=True , blank=True)
    def __str__(self):
         return f"{self.heure_depart}"

class TrajetSegment(models.Model):
    trajet_id = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    segment_id = models.ForeignKey(Segment, on_delete=models.CASCADE)
    prix_segment = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0)

    # place_disponible=models.IntegerField(default=0)

print("Bien ok")
# table intermediaire entre Segment et SegmentHoraire afin de pouvoir gerer les place disponible pour 
# chaque horaire de segment, car un segment ce differencie par leurs horaire 
class SegmentSegmentHoraire(models.Model):
    segment_id = models.ForeignKey(Segment, on_delete=models.CASCADE )
    segmenthoraire_id = models.ForeignKey(SegmentHoraire, on_delete=models.CASCADE)
    place_disponible = models.IntegerField(default=0)


#Pöur modifier les champs  place_disponible pour les instance enregistrer avant 
    print("Commmence BIEN ")
    def save(self, *args, **kwargs):
            print(f"Saving HoraireSegment: segment_id={self.segment_id}, segmenthoraire_id={self.segmenthoraire_id}")

            # Récupérez le trajet associé
            # segment = self.segment_id
            trajet_segments = TrajetSegment.objects.filter(segment_id=self.segment_id)
            print("trajet_segment_HoraireSegment",trajet_segments)


            # Assurez-vous que le trajet a une voiture associée
            if trajet_segments.exists(): 
                trajet = trajet_segments.first().trajet_id
                if trajet.car: 
                # segment_trajet=trajet

                    self.place_disponible = trajet.car.nombre_places

            else :
                print("PLACECECD disponible non enregistrer trajet_segment vide ")

            # Appel à la méthode save de la classe parente pour enregistrer les modifications
            super(SegmentSegmentHoraire, self).save(*args, **kwargs)




@receiver(m2m_changed, sender=Trajet.segments.through , dispatch_uid="segment_instance")
def update_horaire(sender, instance, action,reverse, model, pk_set, **kwargs):
#     #segmentss = Segment.objects.filter(trajet=1)
    # if action == "post_add" or action == "post_clear" :
         

    @receiver(m2m_changed, sender=Trajet.horaires.through, dispatch_uid="horaire_signal")
    def arrets_changed(sender, instance, action, **kwargs):
            if action == "post_add" or action == "post_clear" :
                print("pk_set:",pk_set)
                # print("instance_segement",instance.segments.all())
                for segment in instance.segments.all():
                        # segment = Segment.objects.get(pk=segment_id)
                        print("segments:",segment)
                        if segment.depart == instance.adress_depart:
                            print("horaires:",instance.horaires.all())
                            for horaire in instance.horaires.all():

                                dummy_date = datetime.combine(datetime.today(), horaire.heure_depart)
                                print("je suis dans if")

                                segment.horairesegment.create(heure_depart=dummy_date)
                            segment.save()
                        else:
                                #pre_segments = Segment.objects.get(pk=segment_id)
                            # print("debut elsepreg")

                            for id_segment in pk_set:
                                print("debut presegement")
                                pre_segment = Segment.objects.get(pk=id_segment)
                                # all_segments = list(instance.pre_segment.all())

                                if pre_segment.horairesegment:
                                    # index = all_segments.index(pre_segment)
                                    # prev_segment = all_segments[index - 1]

                                    print('preseg:',pre_segment)
                                    print(pre_segment.horairesegment.all())
                                    if  segment.depart == pre_segment.arrivee:
                                        for horairesegment in pre_segment.horairesegment.all():
                                            print("debut Horaire")


                                            dummy_dat = datetime.combine(datetime.today(), horairesegment.heure_arrivee)
                                            print('dummy_dat', dummy_dat)

                                            # if  segment.depart == pre_segment.arrivee  and dummy_dat:
                                                
                                                    #horairesegss = segment.horairesegment.all()
                                            segment.horairesegment.create(heure_depart=dummy_dat)

                                        segment.save()
                                    else :
                                            for id_segment in pk_set:
                                                prev_segment = Segment.objects.get(pk=id_segment)
                                                if prev_segment.horairesegment:
                                                    for horairesegment in prev_segment.horairesegment.all():
                                                        print("debutOKOKO")
                                                        dummy_dat = datetime.combine(datetime.today(), horairesegment.heure_arrivee)
                                                        new_datetime = dummy_dat + timedelta(minutes=prev_segment.duree)
                    # Convertir datetime en time
                                                        heure_dep = new_datetime.time() 

                                                        # horaire_segment, created = segment.horairesegment.get_or_create(heure_depart=heure_departt)
    
                                                        segment.horairesegment.create(heure_depart=heure_dep)

                                                    segment.save()

                        segment.save()
                
logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=Trajet.segments.through)
def update_segment_prix(sender, instance, action, **kwargs):
    if action == "post_add":
        try:
            nombre_place=instance.car.nombre_places
            car_type = instance.car.type
            for segment in instance.segments.all():
                trajet_segment, created = TrajetSegment.objects.get_or_create(trajet_id = instance, segment_id = segment )
                # trajet_segment.place_disponible=nombre_place
                if car_type.nom == 'Premium':
                    trajet_segment.prix_segment = segment.prix * Decimal('1.375') 
                else:
                    trajet_segment.prix_segment = segment.prix 
                trajet_segment.save()
            logger.info(f"Successfully updated segments and horaires for trajet {instance.pk}")
        except Exception as e:
                    logger.error(f"Error updating segments and horaires for trajet {instance.pk}: {e}")
                    raise
@receiver(m2m_changed, sender=Trajet.segments.through , dispatch_uid="trajet_instance")
def trajet(sender, instance, action,reverse, model, pk_set, **kwargs):
    nombre_place=instance.car.nombre_places
    # car_type = instance.car.type

    @receiver(m2m_changed, sender=Segment.horairesegment.through)
    def update_segment_place(sender, instance, action, **kwargs):
            if action == "post_add":
                
                try:
                    horaires = instance.horairesegment.all()
                    print("HHHORAIREEEE",horaires)
                    for horaire in horaires:
                        horaire_segment, created = SegmentSegmentHoraire.objects.get_or_create( segment_id = instance , segmenthoraire_id = horaire )
                        horaire_segment.place_disponible=nombre_place

                        horaire_segment.save()
                    logger.info(f"Successfully updated segments and horaires for trajet {instance.pk}")
                except Exception as e:
                    logger.error(f"Error updating segments and horaires for trajet {instance.pk}: {e}")
                    raise


    

@receiver(m2m_changed, sender=Segment.horairesegment.through)
def update_heure_arrivee(sender, instance, action, **kwargs):
        if action == "post_add" or action == "post_clear":
            for horaire in instance.horairesegment.all():
                if not horaire.heure_arrivee:
# Convertir heure_depart en datetime
                    dummy_date = datetime.combine(datetime.today(), horaire.heure_depart)
                    # Ajouter la durée
                    new_datetime = dummy_date + timedelta(minutes=instance.duree)
                    # Convertir datetime en time
                    heure_arrivee = new_datetime.time()                    
                    horaire.heure_arrivee = heure_arrivee
                    horaire.save()


# class SegmentHoraire(models.Model):
#     heure_depart = models.TimeField()
#     heure_arrivee = models.TimeField(null=True , blank=True)


#     def __str__(self):
#         #horaires = self.horairesegment.all()  # Récupère tous les SegmentHoraire associés
#         #horaires_str = ", ".join([str(horaire) for horaire in horaires])
#         return f"{self.heure_depart}"

# Attacher le signal pre_save pour exécuter calculer_heures avant la sauvegarde du segmentHoraire
#models.signals.pre_save.connect(SegmentHoraire.calculer_heures, sender=SegmentHoraire)

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)




class Reservation(models.Model):
      
    segmenthoraire_id = models.ForeignKey(SegmentSegmentHoraire,  on_delete=models.CASCADE, related_name='reservations' , null=True)
    client_id = models.ForeignKey(Client, on_delete=models.PROTECT)
    numero_reservation = models.CharField(max_length=100, editable=False, unique=True , null=True , blank=True)  # Numéro de réservation unique
    nombre_de_place = models.IntegerField(default=1)  # Nombre de places réservées
    date_reservation = models.DateTimeField(auto_now_add=True)  # Date de la réservation

    def save(self, *args, **kwargs):
        if not self.numero_reservation:
            # Génère un numéro de réservation unique basé sur l'ID du trajet et un UUID
            self.numero_reservation = f"{self.segmenthoraire_id.id}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)


class Prix_segment(models.Model):
    depart=models.CharField(choices=get_ville_choices, max_length=50)
    arrivee=models.CharField(choices=get_ville_choices,  max_length=50)  
    prix= models.DecimalField(max_digits=10, decimal_places=2)
    duree = models.IntegerField(help_text="Durée en minutes", default=480)


    
