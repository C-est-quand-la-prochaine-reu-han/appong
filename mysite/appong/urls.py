from django.urls import path, include
from . import views

from rest_framework import routers

app_name = "appong"

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserProfileViewSet)
router.register(r'matches', views.MatchViewSet)

urlpatterns = [
	path("api/", include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]