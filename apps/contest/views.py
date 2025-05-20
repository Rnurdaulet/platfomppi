from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.translation import gettext as _

from apps.contest.models import Application
from apps.contest.forms import ApplicationForm
from utils.nca import verify_ecp_signature


class ParticipantRequiredMixin(LoginRequiredMixin):
    """Доступ только участникам"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "participant":
            return HttpResponseForbidden("Доступ только для участников.")
        return super().dispatch(request, *args, **kwargs)


class ApplicationCreateView(ParticipantRequiredMixin, View):
    """Создание новой заявки"""
    def get(self, request):
        if hasattr(request.user, "application"):
            return redirect("contest:application_edit")

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
        app = request.user.application
        if app.is_locked:
            return redirect("contest:application_preview")

        form = ApplicationForm(instance=app, user=request.user)
        return render(request, "contest/application_form.html", {"form": form})

    def post(self, request):
        app = request.user.application
        if app.is_locked:
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
        app = request.user.application
        return render(request, "contest/application_preview.html", {"application": app})


class ApplicationSignView(ParticipantRequiredMixin, View):
    """Подписание заявки — POST с CMS-подписью"""
    def post(self, request):
        import json
        try:
            data = json.loads(request.body)
            cms = data.get("signedData")
            original = data.get("originalData")
            iin, full_name = verify_ecp_signature(cms, original)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

        app = request.user.application
        if app.is_locked:
            return JsonResponse({"success": False, "message": _("Заявка уже подписана.")}, status=400)

        if request.user.username != iin:
            return JsonResponse({"success": False, "message": _("Подпись не соответствует вашему ИИН.")}, status=400)

        app.cms = cms
        app.is_locked = True
        app.save()

        return JsonResponse({"success": True, "redirectUrl": "/"})


