from django.urls import path
from .views import welcome

urlpatterns = [
    path('pet/welcome/', welcome, name='welcome'),
    # Add other URL patterns as needed
]




