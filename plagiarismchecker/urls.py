from django.urls import path
from .views import compare_images, home

urlpatterns = [
    path('', home, name='home'),
]
