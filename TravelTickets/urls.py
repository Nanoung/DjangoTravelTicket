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
    path('TravelTickets_Detail_trajet/<int:id_trajet>/<int:id_segment>/',views.details_trajet, name='detail_trajet'), 
    path('TravelTickets_Reservation/<int:id_trajet>/<int:id_segment>',views.Reservation_trajet, name='detail_segment'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
