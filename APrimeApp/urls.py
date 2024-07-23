from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('studentPreferences', student_preferences, name='studentPreferences'),
    path('categories', get_all_categories, name='get_all_categories'),
]