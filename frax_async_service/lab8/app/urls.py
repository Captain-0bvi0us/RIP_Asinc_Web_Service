from django.urls import path
from app import views

urlpatterns = [
    path('calculate_probability/', views.perform_calculation, name='calc'),
]