from django.urls import path, include
from . import views

from rest_framework import routers

app_name = "appong"

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'login', views.UserProfileViewSet)
router.register(r'user', views.UserProfileViewSet)
router.register(r'match', views.MatchViewSet)
router.register(r'tournament', views.TournamentViewSet)

urlpatterns = [
	path("api/", include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
