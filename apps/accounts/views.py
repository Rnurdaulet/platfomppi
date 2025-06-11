from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, get_user_model
from django.utils.translation import gettext as _, gettext
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.contest.models import Application
from apps.lookups.models import ExpertRegistry, AdminRegistry
from apps.accounts.models import User
from utils.nca import verify_ecp_signature
from django.contrib.auth.models import Group

@method_decorator(csrf_exempt, name="dispatch")
class EcpLoginView(View):
    def get(self, request):
        nonce = User.generate_nonce()
        request.session["ecp_nonce"] = nonce
        return render(request, "accounts/ecp_login.html", {"nonce": nonce})

    def post(self, request):
        import json
        try:
            data = json.loads(request.body)
            signed_data = data["signedData"]
            original_data = data["originalData"]
        except Exception:
            return JsonResponse({"success": False, "message": gettext("Неверный формат запроса.")}, status=400)

        try:
            iin, full_name = verify_ecp_signature(signed_data, original_data)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

        user_model = get_user_model()
        user = None

        # 1. Проверка администратора
        admin = AdminRegistry.objects.filter(iin=iin).first()
        if admin:
            parts = full_name.strip().split()
            last_name = parts[0] if len(parts) > 0 else ""
            first_name = parts[1] if len(parts) > 1 else ""
            user, created = user_model.objects.get_or_create(
                username=iin,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": "admin",
                    "is_active": True,
                    "is_staff": True,
                }
            )
            if not created and user.role != "admin":
                user.role = "admin"
                user.is_staff = True
                user.save()

            if created:
                admins_group, _ = Group.objects.get_or_create(name="Admins")
                user.groups.add(admins_group)

        # 2. Проверка эксперта
        if not user:
            expert = ExpertRegistry.objects.filter(iin=iin).first()
            if expert:
                user, created = user_model.objects.get_or_create(
                    username=iin,
                    defaults={
                        "first_name": expert.first_name,
                        "last_name": expert.last_name,
                        "role": expert.role,
                        "branch": expert.branch,
                        "is_active": True,
                    }
                )
                if not created:
                    updated = False
                    if user.role != expert.role:
                        user.role = expert.role
                        updated = True
                    if hasattr(user, "branch") and user.branch != expert.branch:
                        user.branch = expert.branch
                        updated = True
                    if updated:
                        user.save()

        # 3. Участник (если не найден в двух реестрах)
        if not user:
            parts = full_name.strip().split()
            last_name = parts[0] if len(parts) > 0 else ""
            first_name = parts[1] if len(parts) > 1 else ""
            middlename = parts[2] if len(parts) > 2 else ""
            user, _ = user_model.objects.get_or_create(
                username=iin,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "middlename": middlename,
                    "role": "participant",
                    "is_active": True,
                }
            )

        login(request, user)
        # Проверка наличия заявки
        if user.role == "participant":
            has_application = Application.objects.filter(participant=user).exists()
            if not has_application:
                return JsonResponse({"success": True, "redirectUrl": "/contest/create/"})

        #  Если есть заявка или он эксперт — на главную
        return JsonResponse({"success": True, "redirectUrl": "/"})


from django.conf import settings
from datetime import date

def index(request):
    can_create = date.today() < getattr(settings, "APPLICATION_EDIT_DEADLINE", date.max)
    return render(request, "index.html", {"can_create": can_create})
