from django.urls import path
from apps.contest.views import (
    ApplicationCreateView,
    ApplicationUpdateView,
    ApplicationPreviewView,
    ApplicationSignView,
)

app_name = "contest"

urlpatterns = [
    path("create/", ApplicationCreateView.as_view(), name="application_create"),
    path("edit/", ApplicationUpdateView.as_view(), name="application_edit"),
    path("preview/", ApplicationPreviewView.as_view(), name="application_preview"),
    path("sign/", ApplicationSignView.as_view(), name="application_sign"),
]
