from django.urls import path
from .views import home, get_job_details

urlpatterns = [
    path('', home, name='home'),
    path('jobs/', get_job_details, name='get_job_details'),
]
