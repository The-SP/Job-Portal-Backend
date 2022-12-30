from django.urls import path

from user_system.views import ProfileCreate, ProfileDetailUpdate

urlpatterns = [
    path("profile/create/", ProfileCreate.as_view(), name='profile-create'),
    path("profile/detail/", ProfileDetailUpdate.as_view(), name='profile-detail'),
]
