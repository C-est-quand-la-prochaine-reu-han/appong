from rest_framework import serializers, viewsets, permissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action

from django.http import HttpResponse
from django.contrib.auth.models import User
from ..models import UserProfile

import datetime

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(required=True)

	class Meta:
		model = UserProfile
		fields = ['pk', 'user', 'user_nick', 'avatar']

class UserProfileViewSet(ModelViewSet):
	serializer_class = UserProfileSerializer
	queryset = UserProfile.objects.all().order_by('-user__date_joined')
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	#change name instead of deleting profile
	def delete(self, request, pk, *args, **kwargs):
		instance = UserProfile.objects.get(pk=pk)
		instance.user.username = "deleted" + pk
		instance.user_nick = "deaded" + pk
		instance.user.is_active = False
		instance.avatar = "default_avatar.jpg"
		instance.save()
		#UserProfile.objects.get(pk=pk).delete()
		return HttpResponse("deleted user pk=%s" % pk)

	def create(self, request, *args, **kwargs):
		new_user = User()
		new_user.username = request.POST.get("user_nick")
		new_user.date_joined = datetime.datetime.now()
		new_user.save()
		new_userprofile = UserProfile()
		new_userprofile.user = new_user
		new_userprofile.user_nick = request.POST.get("user_nick")
		if request.POST.get("avatar") != '':
			new_userprofile.avatar = request.POST.get("avatar")
		new_userprofile.save()

		return HttpResponse("created user %s" % new_userprofile.user_nick)
	
	def update(self, request, pk, *args, **kwargs):
		if UserProfile.objects.get(pk=pk).user_nick != request.POST.get("user_nick") and User.objects.filter(username=request.POST.get("user_nick")):
			return HttpResponse("User nick '%s' is not available" % request.POST.get("user_nick"))
		update_user = User.objects.get(username=UserProfile.objects.get(pk=pk).user_nick)
		update_user.username = request.POST.get("user_nick")
		update_user.save()

		update_userprofile = UserProfile.objects.get(pk=pk)
		update_userprofile.user_nick = request.POST.get("user_nick")
		if "avatar" in request.FILES:
			# check somehow the file is valid
			update_userprofile.avatar = request.FILES["avatar"]
		update_userprofile.save()

		return HttpResponse("updated user pk=%s" % update_userprofile.pk)
