from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


app_name = 'APrimeApp'

urlpatterns = [
    path('', index, name='index'),
    path('something/', host_home, name='host_home'),
    path('studentPreferences', student_preferences, name='studentPreferences'),
    path('categories', get_all_categories, name='get_all_categories'),
    path('hostWorkshopDetailsQR/<uuid:workshop_id>/', host_workshop_QR, name='host_workshop_QR'),
    path('registeredworkshops',get_registered_workshops, name='get_registered_workshops'),
    path('workshops/', get_all_workshops, name='get_all_workshops'),
    path('threeworkshops/', get_three_workshops, name='get_three_workshops'),
    path('register', register_for_workshop, name='register_for_workshop'),
    path("cancelworkshop",cancelworkshop, name='cancelworkshop'),
    path("attendance",attendance, name='attendance'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
