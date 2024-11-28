# In urls.py
from django.urls import path
from . import views  # Import the views module

urlpatterns = [
    path('', views.predict_home_price, name='predict_home_price'),
]
