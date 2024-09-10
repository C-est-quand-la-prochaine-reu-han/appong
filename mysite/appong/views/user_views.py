from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from django.http import HttpResponse
from django.contrib.auth.models import User
from ..models import UserProfile
from .serializers import UserProfileSerializer, FriendSerializer

from django.db import IntegrityError

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
		instance.friends_pending.clear()
		instance.friends_confirmed.clear()
		instance.save()
		return HttpResponse("deleted user pk=%s" % pk, status=status.HTTP_204_NO_CONTENT)

	def create(self, request, *args, **kwargs):
		new_user = User()
		new_user.username = request.POST.get("user.username")
		new_user.date_joined = datetime.datetime.now()

		new_userprofile = UserProfile()
		new_userprofile.user = new_user
		new_userprofile.user_nick = request.POST.get("user_nick")
		if "avatar" in request.FILES:
			self.update_avatar(new_userprofile, request.FILES["avatar"])

		try:
			new_user.save()
			new_userprofile.save()
		except IntegrityError as e: #raised by model constraint tourn_name(unique=True)
			return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)
		
		return HttpResponse("created user %s" % new_userprofile.user_nick, status=status.HTTP_201_CREATED)
	
	def update(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_user_nick = request.data.get("user_nick")
		update_userprofile.user_nick = update_user_nick
		if "avatar" in request.FILES:
			self.update_avatar(update_userprofile, request.FILES["avatar"])

		try:
			update_userprofile.save()
		except IntegrityError as e: #raised by model constraint tourn_name(unique=True)
			return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

		return HttpResponse("updated user pk=%s" % update_userprofile.pk, status=status.HTTP_200_OK)

	@action(detail=True, methods=['post'], serializer_class=FriendSerializer)
	def friend_pending(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_userprofile.friends_pending.clear()
		if "friends_pending" in request.POST:
			for value in request.POST.getlist("friends_pending"):
				friend_pending = UserProfile.objects.get(pk=value)
				if update_userprofile.pk == friend_pending.pk:
					return HttpResponse("%s you can't friend yourself" % friend_pending, status=status.HTTP_400_BAD_REQUEST)
				if update_userprofile.friends_confirmed.contains(friend_pending):
					return HttpResponse("%s is already a friend" % friend_pending, status=status.HTTP_400_BAD_REQUEST)
				if update_userprofile.friends_pending.contains(friend_pending) == False:
					update_userprofile.friends_pending.add(friend_pending)
		update_userprofile.save()
		return HttpResponse("updated friends_pending for user=%s" % update_userprofile.pk, status=status.HTTP_200_OK)
	
	@action(detail=True, methods=['post'], serializer_class=FriendSerializer)
	def friend_confirm(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		old_friends = update_userprofile.friends_confirmed.values_list()
		update_userprofile.friends_confirmed.clear()
		if "friends_confirmed" in request.POST:
			for value in request.POST.getlist("friends_confirmed"):
				friend_confirmed = UserProfile.objects.get(pk=value)
				if update_userprofile.friends_confirmed.contains(friend_confirmed) == False \
					and (update_userprofile.friends_pending.contains(friend_confirmed) \
					or old_friends.contains(friend_confirmed)):
					update_userprofile.friends_confirmed.add(friend_confirmed)
					update_userprofile.friends_pending.remove(friend_confirmed)
		update_userprofile.save()
		return HttpResponse("updated friends_confirmed for user=%s" % update_userprofile.pk, status=status.HTTP_200_OK)

	def resize_image(self, image):
		try:
			img = Image.open(image)
			imagename = image.name
		except:
			imagename = "media/default_avatar.jpg"
			img = Image.open(imagename)
		# Resize the image to a desired size (e.g., 300x300)
		resized_img = img.resize((300, 300), resample=Image.BICUBIC)

		# Convert the resized image to bytes
		buffer = BytesIO()
		resized_img.save(buffer, format='png')
		img_bytes = buffer.getvalue()
		img.close()
		
		return (img_bytes, imagename)

	def update_avatar(self, user, file):
		image, file = self.resize_image(file)
		user.avatar.save(file, ContentFile(image), save=False)
