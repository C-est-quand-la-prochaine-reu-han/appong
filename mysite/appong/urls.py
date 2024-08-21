from django.urls import path

from . import views

app_name = "appong"
urlpatterns = [
	path("appong/", include("polls.urls")),
	]