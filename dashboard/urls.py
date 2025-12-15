from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.home_redirect, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # standalone pages
    path("birthday/", TemplateView.as_view(template_name="birthday.html"), name="birthday"),
    path("term/", TemplateView.as_view(template_name="term_countdown.html"), name="term_countdown"),
]
