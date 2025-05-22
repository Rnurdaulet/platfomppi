from django.urls import path

from apps.accounts.views import EcpLoginView, index

urlpatterns = [
    path("login/ecp/", EcpLoginView.as_view(), name="ecp_login"),
    path("", index, name="home"),
]
