from django.urls import path, include
from . import views

app_name = "appong"
urlpatterns = [
	path("", views.User_Index.as_view(), name="users"),
	path("<int:userprofile_id>/", views.User_Detail, name="detail"),
	#path("<int:pk>/", views.User_Detail.as_view(), name="detail"),
	]