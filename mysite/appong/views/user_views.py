from rest_framework import serializers, viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from django.http import HttpResponse
from django.contrib.auth.models import User
from ..models import UserProfile, Friend
from .serializers import UserProfileSerializer

import datetime

class UserProfileViewSet(ModelViewSet):
	serializer_class = UserProfileSerializer
	queryset = UserProfile.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	#change name instead of deleting profile from database
	def delete(self, request, pk, *args, **kwargs):
		instance = UserProfile.objects.get(pk=pk)
		instance.user.username = "deleted" + pk
		instance.user_nick = "deaded" + pk
		instance.user.is_active = False
		instance.avatar = "default_avatar.jpg"
		instance.save()
		# TODO set all friends to NULL
		#UserProfile.objects.get(pk=pk).delete()
		return HttpResponse("deleted user pk=%s" % pk)

	def create(self, request, *args, **kwargs):
		# TODO check user create data is present and valid before saving
		new_user = User()
		new_user.username = request.POST.get("user.username")
		new_user.date_joined = datetime.datetime.now()

		new_userprofile = UserProfile()
		new_userprofile.user = new_user
		new_userprofile.user_nick = request.POST.get("user_nick")
		if "avatar" in request.FILES:
			post_image = request.FILES["avatar"]
			resized_image = self.resize_image(post_image)
			image_name = post_image.name
			new_userprofile.avatar.save(image_name, ContentFile(resized_image), save=False)

		new_user.save()
		new_userprofile.save()

		return HttpResponse("created user %s" % new_userprofile.user_nick)
	
	def update(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_user_nick = request.POST.get("user_nick")

		if update_userprofile.user_nick != update_user_nick \
			and UserProfile.objects.filter(user_nick=update_user_nick):
			return HttpResponse("User nick '%s' is not available" % update_user_nick)

		update_userprofile.user_nick = update_user_nick
		if "avatar" in request.FILES:
			# check somehow the file is valid
			update_userprofile.avatar = request.FILES["avatar"]

		# self.friend_invite(self, request, pk, *args, **kwargs)
		
		if "friends" in request.POST:
			for value in request.POST.getlist("friends"):
				friend_pending = UserProfile.objects.get(pk=value)
				update_userprofile.friends.add(friend_pending)
				friend_status = Friend.objects.filter(user1=update_userprofile, user2=friend_pending)
				friend_status.status = Friend.PENDING_STATUS
			print("-----------%s", friend_status.status)
			# figure out how to show status in api
		
		# if "friends_pending" in request.POST:
		# 	print("-----------%s", request.POST)
		# 	for value in request.POST.getlist("friends_pending"):
		# 		friend_pending = UserProfile.objects.get(pk=value)
		# 		if update_userprofile.pk == friend_pending.pk:
		# 			return HttpResponse("%s you can't friend yourself" % friend_pending)
		# 		if update_userprofile.friends_confirmed.contains(friend_pending):
		# 			return HttpResponse("%s is already a friend" % friend_pending)
		# 		if update_userprofile.friends_pending.contains(friend_pending) == False:
		# 			update_userprofile.friends_pending.add(friend_pending)
		# if "friends_confirmed" in request.POST:
		# 	for value in request.POST.getlist("friends_confirmed"):
		# 		friend_confirmed = UserProfile.objects.get(pk=value)
		# 		if update_userprofile.friends_confirmed.contains(friend_confirmed) == False \
		# 			and update_userprofile.friends_pending.contains(friend_confirmed):
		# 			update_userprofile.friends_confirmed.add(friend_confirmed)
		# 			update_userprofile.friends_pending.remove(friend_confirmed)
		# if "friends_remove" in request.POST:
		# 	for value in request.POST.getlist("friends_remove"):
		# 		update_userprofile.friends_pending.remove(UserProfile.objects.get(pk=value))
		# 		update_userprofile.friends_confirmed.remove(UserProfile.objects.get(pk=value))

		update_userprofile.save()
		return HttpResponse("updated user pk=%s" % update_userprofile.pk)

	# @action(detail=True, methods=['put'])
	# def friend_invite(self, request, pk, *args, **kwargs):
	# 	print(request.PUT)
	# 	return HttpResponse("updated user pk=")# %s" % update_userprofile.pk)

	def resize_image(self, image):
		img = Image.open(image)
		# Resize the image to a desired size (e.g., 300x300)
		resized_img = img.resize((300, 300), resample=Image.BICUBIC)

		# Convert the resized image to bytes
		buffer = BytesIO()
		resized_img.save(buffer, format='png')
		img_bytes = buffer.getvalue()
		img.close()

		return img_bytes