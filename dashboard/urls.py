from django.urls import path
from .views import *

urlpatterns = [
path('', dashboard_redirect, name='dashboard'),
    path('seeker/', seeker_dashboard, name='seeker_dashboard'),
    path('employer/', employer_dashboard, name='employer_dashboard'),
]

