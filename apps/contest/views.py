from datetime import date
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View

from apps.contest.forms import ApplicationForm
from apps.contest.models import Application
from utils.nca import verify_ecp_signature


class ParticipantRequiredMixin(LoginRequiredMixin):
    """Доступ только участникам"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role != "participant":
            return render(request, "403_participant_only.html", status=403)
        return super().dispatch(request, *args, **kwargs)


class ApplicationBaseView(ParticipantRequiredMixin, View):
    """Базовый класс для работы с заявкой"""
    def get_user_application(self, request):
        return Application.objects.filter(participant=request.user).first()


class ApplicationCreateView(ApplicationBaseView):
    """Создание новой заявки"""
    def get(self, request):
        if self.get_user_application(request):
            return redirect("contest:application_edit")

        if date.today() >= getattr(settings, "APPLICATION_EDIT_DEADLINE", date.max):
            messages.error(request, _("Приём заявок завершён."))
            return redirect("home")

        form = ApplicationForm(user=request.user)
        return render(request, "contest/application_form.html", {"form": form})

    def post(self, request):
        if self.get_user_application(request):
            return redirect("contest:application_edit")

        form = ApplicationForm(request.POST, request.FILES, user=request.user)
        if not form.is_valid():
            return render(request, "contest/application_form.html", {"form": form})

        form.save()
        messages.success(request, _("Заявка создана."))
        return redirect("contest:application_preview")


class ApplicationUpdateView(ApplicationBaseView):
    """Редактирование черновика"""
    def get(self, request):
        app = self.get_user_application(request)
        if not app or not app.can_edit():
            messages.warning(request, _("Редактирование заявки недоступно."))
            return redirect("contest:application_preview")

        form = ApplicationForm(instance=app, user=request.user)
        return render(request, "contest/application_form.html", {"form": form})

    def post(self, request):
        app = self.get_user_application(request)
        if not app or not app.can_edit():
            messages.warning(request, _("Редактирование заявки недоступно."))
            return redirect("contest:application_preview")

        form = ApplicationForm(request.POST, request.FILES, instance=app, user=request.user)
        if not form.is_valid():
            return render(request, "contest/application_form.html", {"form": form})

        form.save()
        messages.success(request, _("Изменения сохранены."))
        return redirect("contest:application_preview")


class ApplicationPreviewView(ApplicationBaseView):
    """Просмотр заявки перед подписью"""
    def get(self, request):
        app = self.get_user_application(request)
        if not app:
            messages.warning(request, _("Вы ещё не подали заявку."))
            return redirect("contest:application_create")
        return render(request, "contest/application_preview.html", {"application": app})


class ApplicationSignView(ApplicationBaseView):
    """Подписание заявки — POST с CMS-подписью"""
    def post(self, request):
        app = self.get_user_application(request)
        if not app:
            return JsonResponse({"success": False, "message": _("Заявка не найдена.")}, status=404)

        if app.is_locked:
            return JsonResponse({"success": False, "message": _("Заявка уже подписана.")}, status=400)

        try:
            data = json.loads(request.body)
            cms = data.get("signedData")
            original = data.get("originalData")
            iin, full_name = verify_ecp_signature(cms, original)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

        if request.user.username != iin:
            return JsonResponse({"success": False, "message": _("Подпись не соответствует вашему ИИН.")}, status=400)

        profile = request.user.profile
        if profile and not profile.full_name:
            profile.full_name = full_name
            profile.save()

        app.cms = cms
        app.is_locked = True
        app.save()

        return JsonResponse({"success": True, "redirectUrl": "/"})

def application_chart_view(request):
    return render(request, "contest/applications_stats.html")

from django.db.models import Count
from django.views.decorators.http import require_GET

@require_GET
def application_stats_view(request):
    # Общее количество заявок
    total_applications = Application.objects.count()

    # Подсчёт заявок по регионам
    region_data = (
        Application.objects
        .filter(participant__participant_profile__region__isnull=False)
        .values("participant__participant_profile__region__name_ru")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Подготовка данных в формате для Chart.js
    labels = []
    data = []

    for item in region_data:
        labels.append(item["participant__participant_profile__region__name_ru"])
        data.append(item["count"])

    return JsonResponse({
        "total": total_applications,
        "regions": {
            "labels": labels,
            "data": data,
        }
    })