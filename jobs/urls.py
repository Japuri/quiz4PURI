from django.urls import path
from .views import (
    job_list_view, job_detail_view, JobUpdateView, JobDeleteView,
    job_apply, JobCreateView, job_reject_view
)

app_name = 'jobs'

urlpatterns = [
    path('', job_list_view, name='job_list_view'),
    path('create/', JobCreateView.as_view(), name='job_create_view'),
    path('<int:pk>/', job_detail_view, name='job_detail_view'),
    path('<int:pk>/update/', JobUpdateView.as_view(), name='job_update_view'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='job_delete_view'),
    path('<int:pk>/apply/', job_apply, name='job_apply'),
    path('reject/<int:applicant_id>/', job_reject_view, name='job_reject_view'),
]
