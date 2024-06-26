"""
URL configuration for TravelTickets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from reservations import views
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.rechercher_trajet , name='rechercher_trajet'),
    path('reservation/', views.Reservation_Effectuee , name='reservation'),

    path('TravelTickets_Detail_trajet/<int:id_trajet>/<int:id_segment>/<int:id_horaire>/',views.details_trajet, name='detail_trajet'), 
    path('TravelTickets_Reservation/<int:id_trajet>/<int:id_segment>/<int:id_segmentsegmenthoraire>/',views.Reservation_trajet, name='reservation_trajet'),
    # path('TravelTickets_Travel_tiket/<int:id_trajet>/<int:id_segment>/<int:id_horaire>/',views.Travel_tiket, name='travel_tiket'),
    path('TravelTickets_Travel_tiket/<int:id_trajet>/<int:id_segment>/<int:id_segmentsegmenthoraire>/', views.Ticket, name='ticket'), 
    # path('TicketTelechargement_Travel_tiket/<int:id_reservation>/', views.Telechargement, name='telecharger_ticket'), 



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
