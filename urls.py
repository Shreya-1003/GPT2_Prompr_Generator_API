# gpt2_app/urls.py



from django.urls import path
from .views import generate_text  # Import the view

urlpatterns = [
    path('generate-text/', generate_text, name='generate_text'),  # Define the path
]



