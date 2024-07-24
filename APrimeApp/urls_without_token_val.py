from django.urls import path
from .views_without_token_val import *

urlpatterns = [
    path('', index, name='index'),
    path('studentPreferences', student_preferences, name='studentPreferences'),
    path('categories', get_all_categories, name='categories'),
    path('workshop/<str:workshop_id>/', get_workshop_details, name='get_workshop_details'),
    path('workshop', get_workshop_details, name='get_workshop_details'),
    path('workshops/', get_all_workshops, name='get_all_workshops')
]
