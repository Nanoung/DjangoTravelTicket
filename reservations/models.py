from datetime import *
from decimal import Decimal
from django.utils import timezone
#from datetime import date, datetime, timedelta, timezone
import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.db import transaction



# Create your models here.
"""
class Trajet(models.Model):

    class Type(models.TextChoices):
        VIP='Vip'
        Ordinaire='Ordinaire'

    class Ville(models.TextChoices):
        Korhogo = 'Korhogo'
        Yamoussoukro = 'Yamoussoukro'
        Bouaké = 'Bouaké'
        Abidjan = 'Abidjan'
        

    adress_depart = models.CharField(choices=Ville.choices, max_length=50)
    adress_arrivee = models.CharField(choices=Ville.choices, max_length=50)
    date_depart = models.DateField()
    heure_depart = models.TimeField(null=False)
    heure_arrivee = models.TimeField(null=True)
    distance = models.FloatField(null=True)
    prix = models.IntegerField(null=False)
    type=models.CharField(choices=Type.choices, max_length=50)


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)

class Reservation(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)  # Relation avec le modèle Trajet
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    numero_reservation = models.CharField(max_length=100, editable=False, unique=True)  # Numéro de réservation unique
    nombre_de_place = models.IntegerField()  # Nombre de places réservées
    date_reservation = models.DateField()  # Date de la réservation

    def save(self, *args, **kwargs):
        if not self.numero_reservation:
            # Génère un numéro de réservation unique basé sur l'ID du trajet et un UUID
            self.numero_reservation = f"{self.trajet.id}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)


"""
class Ville(models.TextChoices):
        Korhogo = 'Korhogo'
        Bouaké = 'Bouaké'
        Yamoussoukro = 'Yamoussoukro'
        Abidjan = 'Abidjan'

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
    
class Trajet(models.Model):

    class Type(models.TextChoices):
        VIP='Vip'
        Ordinaire='Ordinaire'

    
    date_str = '2024-01-01'

# Convertir la chaîne de caractères en objet datetime
    #date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

# Utiliser l'objet datetime comme valeur par défaut pour le champ date_depart
    #date_depart = models.DateField(default=date_obj)

    prix = models.DecimalField(max_digits=10, decimal_places=2 , null= True)
    date_depart= models.DateField(default=timezone.now)
    adress_depart=models.CharField(choices=Ville.choices, max_length=50)
    adress_arrivee=models.CharField(choices=Ville.choices, max_length=50)
    nom_voyage=models.CharField(max_length=100 , blank=True)
    horaires = models.ManyToManyField('Horaire',related_name='Trajet')
    segments = models.ManyToManyField('Segment', related_name='Trajet')
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='Trajet' , null=True)  # Relation one-to-many



    def save(self, *args, **kwargs):
        if self.adress_depart and self.adress_arrivee:
            self.nom_voyage = f"{self.adress_depart}_{self.adress_arrivee}"
        super(Trajet, self).save(*args, **kwargs)



"""
@receiver(post_save, sender=Trajet)
def update_segment_prix(sender, instance, **kwargs):
    seg=instance.segments.all()
    print(seg.count())

    print("Signal triggered")
    if instance.car.type.nom == 'Premium':
        for segment in instance.segments.all():
            segment.prix += 1000
            segment.save()
    print(instance.car.type)
"""

class Horaire(models.Model):
    heure_depart = models.TimeField()
    #trajet = models.ManyToManyField('Trajet',related_name='horaire')
    def __str__(self):
       
        return f"{self.heure_depart}"




class Segment(models.Model):
    depart = models.CharField(choices=Ville.choices, max_length=50)
    arrivee = models.CharField(choices=Ville.choices, max_length=50)
    #ordre = models.IntegerField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    duree = models.IntegerField(help_text="Durée en minutes", default=480)
    horairesegment = models.ManyToManyField('SegmentHoraire',related_name='segments',null=True , blank=True)

    def __str__(self):
        horaires = self.horairesegment.all()  # Récupère tous les SegmentHoraire associés
        horaires_str = ", ".join([str(horaire) for horaire in horaires])
        return f" {self.depart} -> {self.arrivee} | Horaires: {horaires_str}"

class TrajetSegment(models.Model):
    trajet_id = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    segment_id = models.ForeignKey(Segment, on_delete=models.CASCADE)
    prix_segment = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0)
    place_disponible=models.IntegerField(default=0)

print("Bien ok")

"""
#Pöur modifier les champs  place_disponible pour les instance enregistrer avant 
    def save(self, *args, **kwargs):
        # Récupérez le trajet associé
        trajet = self.trajet_id
        
        # Assurez-vous que le trajet a une voiture associée
        if trajet and trajet.car:
            self.place_disponible = trajet.car.nombre_places

        # Appel à la méthode save de la classe parente pour enregistrer les modifications
        super(TrajetSegment, self).save(*args, **kwargs)




@receiver(m2m_changed, sender=Trajet.segments.through)
def update_horaire(sender, instance, action, **kwargs):
        horaires = instance.horaires.all()
        segments = instance.segments.all()

        if action == "post_add" or action == "post_clear":
           
                for segment in segments:
            # Si c'est le premier segment du trajet, il doit partir à l'heure de départ du trajet
                    if segment.depart == instance.depart:
                        for horaire in horaires :
                            segment.horairesegment.heure_depart = horaire.heure_depart
                        segment.horairesegment.save()

                            

            # Pour les segments restants, trouver l'heure de départ en fonction de l'heure d'arrivée du segment précédent
                    else:
                        for prev_segment in segments:
                            if prev_segment.arrivee == segment.depart and prev_segment.horairesegment.heure_arrivee:
                                for horaire_prev in  prev_segment.horairesegment :

                                    segment.horairesegment.heure_depart=prev_segment.horaire_prev.heure_arrivee 
                                    break
                                segment.horairesegment.save()

        # Convertir heure_depart en datetime
                    for horair in segment.horairesegment:
                        dummy_date = datetime.combine(datetime.today(), horair.heure_depart)
                                # Ajouter la durée
                        new_datetime = dummy_date + timedelta(minutes=segment.duree)
                                # Convertir datetime en time
                        heure_arrivee = new_datetime.time()                    
                        horair.heure_arrivee = heure_arrivee
                        horair.save()

print("Bien kkk")

@receiver(m2m_changed, sender=Trajet.segments.through)
def update_other_segments(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add" or action == "post_clear":
        print("Bien joué")

        with transaction.atomic():
            tajet_segment, created = Segment.objects.get_or_create(
                depart=instance.adress_depart, 
                arrivee=instance.adress_arrivee, 
                prix=instance.prix
            )
            try:
                instance.segments.add(tajet_segment)
                print("ajout du segment : ")

            except Exception as e:
                print("Erreur lors de l'ajout du segment : ")

    instance.save()

"""


@receiver(m2m_changed, sender=Trajet.segments.through)
def update_horaire(sender, instance, action,reverse, model, pk_set, **kwargs):
    #segmentss = Segment.objects.filter(trajet=1)
    if action == "post_add" or action == "post_clear" :
        
        
        with transaction.atomic():
            tajet_segment, created = Segment.objects.get_or_create(
                depart=instance.adress_depart, 
                arrivee=instance.adress_arrivee, 
                prix=instance.prix
            )
            try:
                instance.segments.add(tajet_segment)
                print("ajout du segment : ")

            except Exception as e:
                print("Erreur lors de l'ajout du segment : ")


        for segment_id in pk_set:
            segment = Segment.objects.get(pk=segment_id)
            if segment.depart == instance.adress_depart:

                for horaire in instance.horaires.all():

                    dummy_date = datetime.combine(datetime.today(), horaire.heure_depart)
                    #print("je suis dans if")

                    segment.horairesegment.create(heure_depart=dummy_date)
            else:
                    #pre_segments = Segment.objects.get(pk=segment_id)

                for segment_id in pk_set:
                    pre_segment = Segment.objects.get(pk=segment_id)

                    for horairesegment in pre_segment.horairesegment.all():
                        dummy_dat = datetime.combine(datetime.today(), horairesegment.heure_arrivee)

                        if  segment.depart == pre_segment.arrivee  and dummy_dat:

                                #horairesegss = segment.horairesegment.all()
                            segment.horairesegment.create(heure_depart=dummy_dat)
            segment.save()
                
"""
        for segment in instance.segments.all():
            if segment.depart == instance.adress_depart:
                print("je suis dans if")

                for horaire in instance.horaires.all():
                    print(horaire)
                    horairesegs = segment.horairesegment.all()  # Récupère tous les SegmentHoraire associés
                    for horaireseg in horairesegs:
                        if not horaireseg.heure_depart:
                            horaireseg.heure_depart = horaire.heure_depart
                            horaireseg.save()
            else:

                print("je suis dans else")
                for prev_segment in instance.segments.all():
                    print(prev_segment)
                    for horairesseg in prev_segment.horairesegment():
                        if prev_segment.arrivee == segment.depart and horairesseg.heure_arrivee:
                            horairesegss = segment.horairesegment.all()
                            for heurs in horairesegss:
                                if not heurs.heure_depart:
                                    heurs.heure_depart = horairesseg.heure_arrivee
                                    heurs.save()
        # Calculer l'heure d'arrivée en ajoutant la durée au départ
        for segment in instance.segments.all():
            for horai in segment.horairesegment():

                dummy_date = datetime.combine(datetime.today(), horai.heure_depart)
                new_datetime = dummy_date + timedelta(minutes=segment.duree)
                horai.heure_arrivee = new_datetime.time()
                horai.save()
"""
@receiver(m2m_changed, sender=Trajet.segments.through)
def update_segment_prix(sender, instance, action, **kwargs):
    if action == "post_add":
        nombre_place=instance.car.nombre_places
        car_type = instance.car.type
        for segment in instance.segments.all():
            trajet_segment, created = TrajetSegment.objects.get_or_create(trajet_id = instance, segment_id = segment )
            trajet_segment.place_disponible=nombre_place
            if car_type.nom == 'Premium':
                trajet_segment.prix_segment = segment.prix * Decimal('1.375') 
            else:
                trajet_segment.prix_segment = segment.prix 
            trajet_segment.save()


    

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

"""


    def save(self, *args, **kwargs):
        if not self.ordre:
            # Définir l'ordre par défaut ou calculé ici
            dernier_ordre=Trajet.Segment.All().aggregate(max_ordre=max('ordre'))['max_ordre'] or 0
            self.ordre = dernier_ordre + 1
        super().save(*args, **kwargs)

    
    def save(self, *args, **kwargs):
        if not self.pk:  # Si c'est un nouveau segment
            self.ordre = self.Trajet.Segments.count() + 1  # Calculez l'ordre
        super().save(*args, **kwargs)
"""
class SegmentHoraire(models.Model):
    heure_depart = models.TimeField()
    heure_arrivee = models.TimeField(null=True , blank=True)


    def __str__(self):
        #horaires = self.horairesegment.all()  # Récupère tous les SegmentHoraire associés
        #horaires_str = ", ".join([str(horaire) for horaire in horaires])
        return f"{self.heure_depart}"

"""
@receiver(pre_save, sender=Segment)

def calculer_heures(sender, instance, **kwargs):
        # Obtenez le trajet associé
        trajet = instance.Trajet

        # Obtenez l'horaire associé
        try:
            horaire = Trajet.Horaire.all()
            #heure_depart_trajet = datetime.combine(trajet.date_depart, horaire.heure_depart)
        except Horaire.DoesNotExist:
            heure_depart_trajet = timezone.now()

        # Si l'adresse de départ du segment correspond à celle du trajet
        if instance.depart == trajet.adress_depart:
            for horaire in horaire:

                instance.horairesegment.heure_depart = horaire.heure_depart

        else:
                instance.horairesegment.heure_depart = timezone.now()

        elif not instance.SegmentHoraire.heure_depart:
            # Trouvez le segment précédent dans l'ordre
            try:
                dernier_segments = Trajet.instance.objects.filter( ordre=instance.ordre - 1).latest('ordre')
                if dernier_segments.arrivee == instance.depart:
                    for dernier_segment in dernier_segments:

                        instance.horairesegment.heure_depart = dernier_segment.heure_arrivee
                else:
                    instance.heure_depart = timezone.now()
            except Segment.DoesNotExist:
                instance.horairesegment.heure_depart = timezone.now()
            
        # Calculez l'heure d'arrivée
        if not instance.horairesegment.heure_arrivee:
            instance.horairesegment.heure_arrivee = instance.horairesegment.heure_depart + timedelta(minutes=instance.duree)
        """
# Attacher le signal pre_save pour exécuter calculer_heures avant la sauvegarde du segmentHoraire
#models.signals.pre_save.connect(SegmentHoraire.calculer_heures, sender=SegmentHoraire)

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)




class Reservation(models.Model):
      # Relation avec le modèle Trajet
    trajet_id = models.ForeignKey('Trajet', on_delete=models.CASCADE, related_name='reservations' , null=True)     
    segment_id = models.ForeignKey('Segment',  on_delete=models.CASCADE, related_name='reservations' , null=True)
    client_id = models.ForeignKey(Client, on_delete=models.PROTECT)
    numero_reservation = models.CharField(max_length=100, editable=False, unique=True , null=True , blank=True)  # Numéro de réservation unique
    nombre_de_place = models.IntegerField(default=1)  # Nombre de places réservées
    date_reservation = models.DateTimeField(auto_now_add=True)  # Date de la réservation

    def save(self, *args, **kwargs):
        if not self.numero_reservation:
            # Génère un numéro de réservation unique basé sur l'ID du trajet et un UUID
            self.numero_reservation = f"{self.trajet.id}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    
