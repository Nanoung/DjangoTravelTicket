from datetime import *
from django.utils import timezone
#from datetime import date, datetime, timedelta, timezone
import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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


class Type(models.TextChoices):
        standard = 'Standard'
        premium = 'Premium'
        

class CarType(models.Model):
    nom = models.CharField(choices=Type.choices, max_length=100)
    avantages = models.ManyToManyField(Avantage, related_name='car_types')



class Cars(models.Model):

    immatriculation = models.CharField(max_length=100)
    nombre_places = models.IntegerField()
    type = models.ForeignKey(CarType, on_delete=models.CASCADE, related_name='cars')
# Cela permet d'accéder à toutes les voitures d'un type de voiture spécifique en utilisant car_type.cars.all()
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

class Horaire(models.Model):
    heure_depart = models.TimeField()
    #trajet = models.ManyToManyField('Trajet',related_name='horaire')



class Segment(models.Model):
    depart = models.CharField(choices=Ville.choices, max_length=50)
    arrivee = models.CharField(choices=Ville.choices, max_length=50)
    ordre = models.IntegerField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    duree = models.IntegerField(help_text="Durée en minutes")
    horairesegment = models.ManyToManyField('SegmentHoraire',related_name='Segment',blank=True)
    """
    def save(self, *args, **kwargs):
        if not self.ordre:
            # Définir l'ordre par défaut ou calculé ici
            dernier_ordre=Trajet.Segment.All().aggregate(max_ordre=max('ordre'))['max_ordre'] or 0
            self.ordre = dernier_ordre + 1
        super().save(*args, **kwargs)
"""
    def __str__(self):
        return f"Segment {self.ordre}: {self.depart} -> {self.arrivee}"
    
    """
    def save(self, *args, **kwargs):
        if not self.pk:  # Si c'est un nouveau segment
            self.ordre = self.Trajet.Segments.count() + 1  # Calculez l'ordre
        super().save(*args, **kwargs)
    """
class SegmentHoraire(models.Model):
    heure_depart = models.TimeField()
    heure_arrivee = models.TimeField()


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

                """
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
            """
        # Calculez l'heure d'arrivée
        if not instance.horairesegment.heure_arrivee:
            instance.horairesegment.heure_arrivee = instance.horairesegment.heure_depart + timedelta(minutes=instance.duree)

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
    numero_reservation = models.CharField(max_length=100, editable=False, unique=True)  # Numéro de réservation unique
    nombre_de_place = models.IntegerField()  # Nombre de places réservées
    date_reservation = models.DateTimeField(auto_now_add=True)  # Date de la réservation

    def save(self, *args, **kwargs):
        if not self.numero_reservation:
            # Génère un numéro de réservation unique basé sur l'ID du trajet et un UUID
            self.numero_reservation = f"{self.trajet.id}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    
