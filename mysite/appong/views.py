from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse # gets full url from this side to return a redirect to the client
from django.views import generic
from django.db.models import F
from django.shortcuts import render, get_object_or_404 # Render: combines a given template with a given context dictionary and returns an HttpResponse object with that rendered text.

from .models import UserProfile, Match, Tournament

# UserProfile

class User_Index(generic.ListView):
	template_name = "appong/user_index.html"
	context_object_name = "user_list"
	def get_queryset(self):
		"""Return the user list."""
		return UserProfile.objects.all()

# class User_Detail(generic.DetailView):
# 	model = UserProfile # Question inherits from models.Model
# 	template_name = "appong/user_detail.html"

def User_Detail(request, userprofile_id):
	user_nick = UserProfile.objects.get(id=userprofile_id).user_nick
	user_avatar = UserProfile.objects.get(id=userprofile_id).avatar
	return HttpResponse(user_avatar, content_type="image/png")
	return HttpResponse("You're looking at profile %s." % user_nick)

def User_Update(request, userprofile_id):
	pass

def User_Create(request, userprofile_id):
	pass

def User_Delete(request, userprofile_id):
	pass