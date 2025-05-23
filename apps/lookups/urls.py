from django.urls import path
from apps.lookups.autocomplete import PositionAutocomplete, SubjectAutocomplete, SchoolAutocomplete

urlpatterns = [
    path("position-autocomplete/", PositionAutocomplete.as_view(), name="position-autocomplete"),
    path("subject-autocomplete/", SubjectAutocomplete.as_view(), name="subject-autocomplete"),
    path("school-autocomplete/", SchoolAutocomplete.as_view(), name="school-autocomplete"),
]
