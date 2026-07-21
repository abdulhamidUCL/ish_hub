from django.urls import path
from .views import *

urlpatterns = [
    path('create/', company_create, name='company_create'),
    path('company_edit/', company_edit, name='company_edit'),
    path('company_detail/', company_detail, name='company_detail'),
]

