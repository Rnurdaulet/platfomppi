from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    path("admin/", admin.site.urls),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", lambda request: render(request, "index.html"), name="home"),
    path("privacy", lambda request: render(request, "privacy.html"), name="privacy"),
    path("404", lambda request: render(request, "404.html"), name="404"),
    path("", include("apps.accounts.urls")),
    path("contest/", include("apps.contest.urls", namespace="contest")),
)
