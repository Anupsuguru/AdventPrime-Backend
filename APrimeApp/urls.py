from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('studentPreferences', student_preferences, name='studentPreferences'),
    path('categories', get_all_categories, name='get_all_categories'),
    path('registeredworkshops',get_registered_workshops, name='get_registered_workshops'),
    path('workshops/', get_all_workshops, name='get_all_workshops'),
    path('threeworkshops/', get_three_workshops, name='get_three_workshops'),
    path('register', register_for_workshop, name='register_for_workshop'),
    path("cancelworkshop",cancelworkshop, name='cancelworkshop'),
    path("attendance",attendance, name='attendance'),
    
    
]
