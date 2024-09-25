from rest_framework.authtoken import views as drfviews
from rest_framework import routers

from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = "appong"

router = routers.DefaultRouter()
router.register(r"user", views.UserProfileViewSet)
router.register(r"register", views.RegisterUserViewSet, basename="register")
router.register(r"match", views.MatchViewSet)
router.register(r"tournament", views.TournamentViewSet)

urlpatterns = [
	path("api/", include(router.urls)),
	path("api-auth/", drfviews.obtain_auth_token)
]
