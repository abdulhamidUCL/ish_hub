from django.urls import path
from .views import *

urlpatterns = [
    path('create_job/', create_job, name='create_job'),
    path('view_job/<int:job_id>/', view_job, name='view_job'),
    path('edit_job/<int:job_id>/', edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', delete_job, name='delete_job'),
    path('job_list/', job_list, name='job_list'),
    path('job_search/', job_search, name='job_search'),
    path('my_jobs/', my_jobs, name='my_jobs'),
    path('update_status/<int:application_id>/', UpdateApplicationStatus.as_view(), name='update_application_status'),
]
