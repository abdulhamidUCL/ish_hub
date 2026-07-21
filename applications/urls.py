from django.urls import path
from .views import *

urlpatterns = [
    path('job_apply/<int:job_id>', job_apply, name='job_apply'),
    path('my_applications', my_applications, name='my_applications'),
    path('all_applications', all_applications, name='all_applications'),
    path('job/<int:job_id>/applicants/', applicant_list, name='applicant_list'),
    path('applicant/<int:application_id>/', applicant_detail, name='applicant_detail'),
    path('applicant/<int:application_id>/accept/', accept_application, name='accept_application'),
    path('applicant/<int:application_id>/reject/', reject_application, name='reject_application'),
]
