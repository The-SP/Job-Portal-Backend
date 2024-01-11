from django.urls import path
from .views import ApplicantRankingView

urlpatterns = [
    path(
        "applicant-ranking/<int:pk>/",
        ApplicantRankingView.as_view(),
        name="applicant-ranking",
    ),
]
