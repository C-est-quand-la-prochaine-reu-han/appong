from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from appong.views import UserDashboard

from rest_framework.authtoken import views as drfviews
from rest_framework import routers

app_name = "appong"

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"user", views.UserProfileViewSet)
router.register(r"match", views.MatchViewSet)
router.register(r"tournament", views.TournamentViewSet)
router.register(r"dashboard", UserDashboard, basename="dashboard")

urlpatterns = [
	path("api/", include(router.urls)),
	path("api-auth/", drfviews.obtain_auth_token)
]
