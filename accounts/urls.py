import profile

from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('view_profile/<int:pk>/', view_profile, name='view_profile'),
    path('edit_resume/', edit_resume, name='edit_resume'),
]

