from django.urls import path

from .views_api import (ChangePasswordAPI, LoginAPI, LogoutAPI, ProfileAPI,
                        RegisterAPI)

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="api_register"),
    path("login/", LoginAPI.as_view(), name="api_login"),
    path("logout/", LogoutAPI.as_view(), name="api_logout"),
    path("profile/", ProfileAPI.as_view(), name="api_profile"),
    path("change-password/", ChangePasswordAPI.as_view(), name="api_change_password"),
]
