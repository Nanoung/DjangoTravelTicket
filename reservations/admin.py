from django.contrib import admin

from reservations.models import Arret, Avantage, CarType, Cars, Client, Horaire, Reservation, Segment, SegmentHoraire, Trajet, Ville

class TrajetAdmin(admin.ModelAdmin):
    list_display = ( 'id','adress_depart','adress_arrivee')
    exclude = ('nom_voyage',)
    class Media:
        js = ('jsStyle/script_admin.js',)


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
class VilleAdmin(admin.ModelAdmin):
    list_display =('id','nom','ordre')
    
class ArretAdmin(admin.ModelAdmin):
    list_display =('id','ville')

    class Media:
        js = ('jsStyle/script_admin.js',)


        

admin.site.register(Trajet,TrajetAdmin) #permet de faire mise a jour de admin
admin.site.register(Avantage,AvantageAdmin) #permet de faire mise a jour de admin
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Cars,CarsAdmin)
admin.site.register(Horaire,HoraireAdmin)
admin.site.register(Segment,SegmentAdmin)
admin.site.register(CarType,CarTypeAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(SegmentHoraire,SegmentHoraireAdmin)
admin.site.register(Arret,ArretAdmin)
admin.site.register(Ville,VilleAdmin)





# Register your models here.
