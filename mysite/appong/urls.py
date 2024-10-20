from rest_framework.authtoken import views as drfviews
from rest_framework import routers

from django.urls import path, re_path, include
from django.views.generic import TemplateView

from django.conf import settings

from django.views.static import serve

from . import views

app_name = "appong"

router = routers.DefaultRouter()
router.register(r"user", views.UserProfileViewSet)
router.register(r"register", views.RegisterUserViewSet, basename="register")
router.register(r"match", views.MatchViewSet)
router.register(r"tournament", views.TournamentViewSet)

urlpatterns = [
	path("api/", include(router.urls)),
	re_path(r'^api/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
	path("api-auth/", drfviews.obtain_auth_token)
]
