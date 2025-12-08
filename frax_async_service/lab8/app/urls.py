from django.urls import path
from app import views

urlpatterns = [
    path('calc/', views.perform_calculation, name='calc'),
]