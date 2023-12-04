# quiz_app/urls.py

from django.urls import path
from .views import quiz, view_results

urlpatterns = [
    path('quiz/', quiz, name='quiz'),
    path('results/', view_results, name='view_results'),
    # Add other URLs as needed
]
