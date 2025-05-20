from django.urls import path

from apps.accounts.views import EcpLoginView

urlpatterns = [
    path("login/ecp/", EcpLoginView.as_view(), name="ecp_login"),
]
