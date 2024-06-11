from django.contrib import admin

from reservations.models import Avantage, CarType, Cars, Client, Horaire, Reservation, Segment, SegmentHoraire, Trajet

class TrajetAdmin(admin.ModelAdmin):
    list_display = ( 'id','adress_depart','adress_arrivee')


class ClientAdmin(admin.ModelAdmin):
    list_display =('id','nom')

class AvantageAdmin(admin.ModelAdmin):
    list_display =('id','nom','description')
class ReservationAdmin(admin.ModelAdmin):
    list_display =('id','trajet_id','segment_id', 'client_id','numero_reservation', 'date_reservation')
class CarsAdmin(admin.ModelAdmin):
    list_display =('id','immatriculation','nombre_places','type')

class HoraireAdmin(admin.ModelAdmin):
    time_format = '%H:%M'
    list_display =('id','heure_depart')

class SegmentAdmin(admin.ModelAdmin):
    list_display =('id','depart','arrivee','duree','prix')

class CarTypeAdmin(admin.ModelAdmin):
    list_display =('id','nom')
    

class SegmentHoraireAdmin(admin.ModelAdmin):
    time_format = '%H:%M'
    list_display =('id','heure_depart','heure_arrivee')

    



admin.site.register(Trajet,TrajetAdmin) #permet de faire mise a jour de admin
admin.site.register(Avantage,AvantageAdmin) #permet de faire mise a jour de admin
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Cars,CarsAdmin)
admin.site.register(Horaire,HoraireAdmin)
admin.site.register(Segment,SegmentAdmin)
admin.site.register(CarType,CarTypeAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(SegmentHoraire,SegmentHoraireAdmin)



# Register your models here.
