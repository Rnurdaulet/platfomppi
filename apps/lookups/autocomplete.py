from dal import autocomplete
from django.db.models import Q

from apps.lookups.models import Position, Subject, School


class PositionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Position.objects.none()

        qs = Position.objects.all()
        if self.q:
            qs = qs.filter(Q(name_ru__icontains=self.q) | Q(name_kk__icontains=self.q))
        return qs


class SubjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Subject.objects.none()

        qs = Subject.objects.all()
        if self.q:
            qs = qs.filter(Q(name_ru__icontains=self.q) | Q(name_kk__icontains=self.q))
        return qs


class SchoolAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return School.objects.none()

        region_id = self.forwarded.get("region")
        qs = School.objects.all()
        if region_id:
            qs = qs.filter(region_id=region_id)

        if self.q:
            qs = qs.filter(Q(name_ru__icontains=self.q) | Q(name_kk__icontains=self.q))

        return qs
