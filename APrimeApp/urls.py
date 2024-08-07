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
    path('hostWorkshopDetailsQR/<int:workshop_id>/', host_workshop_QR, name='host_workshop_QR'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
