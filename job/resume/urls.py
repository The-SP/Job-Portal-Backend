from django.urls import path
from .views import *

urlpatterns = [
    path("education/", EducationCreateView.as_view(), name="education-create"),
    path("education/<int:pk>/", EducationDetailView.as_view(), name="education-detail"),
]
