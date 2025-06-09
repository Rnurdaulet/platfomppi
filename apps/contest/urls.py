from django.urls import path
from apps.contest.views import (
    ApplicationCreateView,
    ApplicationUpdateView,
    ApplicationPreviewView,
    ApplicationSignView, application_stats_view, application_chart_view, application_table_data_view,
)

app_name = "contest"

urlpatterns = [
    path("create/", ApplicationCreateView.as_view(), name="application_create"),
    path("edit/", ApplicationUpdateView.as_view(), name="application_edit"),
    path("preview/", ApplicationPreviewView.as_view(), name="application_preview"),
    path("sign/", ApplicationSignView.as_view(), name="application_sign"),
    path("api/stats/applications/", application_stats_view, name="application_stats"),
    path("stats/", application_chart_view, name="application_chart"),
path("api/stats/table-data/", application_table_data_view, name="application_table_data"),
]
