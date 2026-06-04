from django.urls import path

from .views import (
    CompanyTaskListAPIView,
    CompanyTaskResubmitAPIView,
    CompanyTaskSubmitAPIView,
    CompanyTaskDetailAPIView,
)

urlpatterns = [
    path("", CompanyTaskListAPIView.as_view(), name="company-task-list"),
    path("submit/", CompanyTaskSubmitAPIView.as_view(), name="company-task-submit"),
    path("<str:task_id>/resubmit/", CompanyTaskResubmitAPIView.as_view(), name="company-task-resubmit"),
    path("<str:task_id>/", CompanyTaskDetailAPIView.as_view(), name="company-task-detail"),
]
