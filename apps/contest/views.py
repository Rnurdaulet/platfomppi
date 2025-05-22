from datetime import date
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
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


class ApplicationCreateView(ParticipantRequiredMixin, View):
    """Создание новой заявки"""
    def get(self, request):
        if hasattr(request.user, "application"):
            return redirect("contest:application_edit")

        can_create = date.today() < getattr(settings, "APPLICATION_EDIT_DEADLINE", date.max)
        if not can_create:
            messages.error(request, _("Приём заявок завершён."))
            return redirect("home")

        form = ApplicationForm(user=request.user)
        return render(request, "contest/application_form.html", {"form": form})

    def post(self, request):
        if hasattr(request.user, "application"):
            return redirect("contest:application_edit")

        form = ApplicationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            app = form.save(commit=False)
            app.participant = request.user
            app.save()
            messages.success(request, _("Заявка создана."))
            return redirect("contest:application_preview")
        return render(request, "contest/application_form.html", {"form": form})


class ApplicationUpdateView(ParticipantRequiredMixin, View):
    """Редактирование черновика"""
    def get(self, request):
        app = getattr(request.user, "application", None)
        if not app or not app.can_edit():
            messages.warning(request, _("Редактирование заявки недоступно."))
            return redirect("contest:application_preview")

        form = ApplicationForm(instance=app, user=request.user)
        return render(request, "contest/application_form.html", {"form": form})

    def post(self, request):
        app = getattr(request.user, "application", None)
        if not app or not app.can_edit():
            messages.warning(request, _("Редактирование заявки недоступно."))
            return redirect("contest:application_preview")

        form = ApplicationForm(request.POST, request.FILES, instance=app, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Изменения сохранены."))
            return redirect("contest:application_preview")
        return render(request, "contest/application_form.html", {"form": form})


class ApplicationPreviewView(ParticipantRequiredMixin, View):
    """Просмотр заявки перед подписью"""
    def get(self, request):
        app = getattr(request.user, "application", None)
        if not app:
            messages.warning(request, _("Вы ещё не подали заявку."))
            return redirect("contest:application_create")
        return render(request, "contest/application_preview.html", {"application": app})


class ApplicationSignView(ParticipantRequiredMixin, View):
    """Подписание заявки — POST с CMS-подписью"""
    def post(self, request):
        app = getattr(request.user, "application", None)
        if not app:
            return JsonResponse({"success": False, "message": _("Заявка не найдена.")}, status=404)

        try:
            data = json.loads(request.body)
            cms = data.get("signedData")
            original = data.get("originalData")
            iin, full_name = verify_ecp_signature(cms, original)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

        if app.is_locked:
            return JsonResponse({"success": False, "message": _("Заявка уже подписана.")}, status=400)

        if request.user.username != iin:
            return JsonResponse({"success": False, "message": _("Подпись не соответствует вашему ИИН.")}, status=400)

        app.cms = cms
        app.is_locked = True
        app.save()

        return JsonResponse({"success": True, "redirectUrl": "/"})
