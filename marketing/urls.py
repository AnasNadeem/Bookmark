from .views import extension_package
from django.urls import path


urlpatterns = [
    path('extension/', extension_package),
]
