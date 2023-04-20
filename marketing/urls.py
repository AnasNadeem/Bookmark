from .views import extension_package, index
from django.urls import path


urlpatterns = [
    path('', index),
    path('extension/', extension_package),
]
