from django.urls import path
from .views import *

urlpatterns = [
    path("recommendations/", JobRecommendationsList.as_view(), name="recommended-jobs"),
]
