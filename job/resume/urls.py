from django.urls import path
from .views import *

urlpatterns = [
    path("education/", EducationListCreateView.as_view(), name="education-create"),
    path("education/<int:pk>/", EducationDetailView.as_view(), name="education-detail"),
    path("experience/", ExperienceListCreateView.as_view(), name="experience-create"),
    path(
        "experience/<int:pk>/", ExperienceDetailView.as_view(), name="experience-detail"
    ),
    path("project/", ProjectListCreateView.as_view(), name="project-create"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("skill/", SkillListCreateView.as_view(), name="skill-create"),
    path("skill/<int:pk>/", SkillDetailView.as_view(), name="skill-detail"),
    path("interest/", InterestListCreateView.as_view(), name="interest-create"),
    path("interest/<int:pk>/", InterestDetailView.as_view(), name="interest-detail"),
    path("award/", AwardListCreateView.as_view(), name="award-create"),
    path("award/<int:pk>/", AwardDetailView.as_view(), name="award-detail"),
]
