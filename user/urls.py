from django.urls import path
from .views import CustomLoginView,ProfileView
from django.contrib.auth.views import LogoutView
from .views import RegisterView 
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import static





urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    
]
