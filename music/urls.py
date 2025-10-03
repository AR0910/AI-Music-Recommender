from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ensure this line is present
    path('recommend/', views.recommend, name='recommend'),  # Add the recommend route here
]
