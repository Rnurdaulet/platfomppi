from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("admin/", admin.site.urls),  # админка всегда на русском
    path("logout/", LogoutView.as_view(), name="logout"),
    path("i18n/", include("django.conf.urls.i18n")),  # переключение языка
]

urlpatterns += i18n_patterns(
    path("", include("apps.accounts.urls")),
)
