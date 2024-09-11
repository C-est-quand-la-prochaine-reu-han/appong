from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes

from django.http import HttpResponse
from django.contrib.auth.models import User
from ..models import UserProfile
from .serializers import UserProfileSerializer, FriendSerializer

from django.db import IntegrityError
from django.core.exceptions import ValidationError


class UserProfileViewSet(ModelViewSet):
	serializer_class = UserProfileSerializer
	queryset = UserProfile.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	#change name instead of deleting profile from database
	def delete(self, request, pk, *args, **kwargs):
		delete_userprofile = UserProfile.objects.filter(pk=pk)
		if delete_userprofile.count() == 1:
			delete_userprofile[0].anonymise()

		context = "deleted user pk=%s" % pk
		return HttpResponse(context, status=status.HTTP_204_NO_CONTENT)

	def create(self, request, *args, **kwargs):
		# new_userprofile = UserProfile(request)
		# new_user = User()
		# new_user.username = request.data.get("user.username")
		# new_user.date_joined = datetime.datetime.now()

		# new_userprofile = UserProfile()
		# new_userprofile.user = new_user
		# new_userprofile.user_nick = request.data.get("user_nick")
		# if "avatar" in request.FILES:
		# 	new_userprofile.update_avatar(new_userprofile, request.FILES["avatar"])
		try:
			print(request.data.get("user.username"))
			UserProfile.objects.create_userprofile(
				request.data.get("user.username"),
				request.data.get("user.password"),
				request.data.get("user_nick"),
				avatar=request.FILES.get("avatar")
			)
		except ValidationError as e: #raised by user model validation
			return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)
		except IntegrityError as e: #raised by model constraint (unique=True)
			return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)
		
		context = "created user %s" % request.data.get("user_nick")
		return HttpResponse(context, status=status.HTTP_201_CREATED)
	
	def update(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_user_nick = request.data.get("user_nick")
		update_userprofile.user_nick = update_user_nick
		if "avatar" in request.FILES:
			update_userprofile.update_avatar(update_userprofile, request.FILES["avatar"])

		try:
			update_userprofile.save()
		except IntegrityError as e: #raised by model constraint tourn_name(unique=True)
			return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

		context = "updated user pk=%s" % update_userprofile.pk
		return HttpResponse(context, status=status.HTTP_200_OK)

	@action(detail=True, methods=['post'], serializer_class=FriendSerializer)
	def friend_pending(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_userprofile.friends_pending.clear()

		if "friends_pending" in request.POST:
			update_userprofile.add_to_pending(request.POST.getlist("friends_pending"))

		context = "updated friends_pending for user=%s" % update_userprofile.pk
		return HttpResponse(context, status=status.HTTP_200_OK)
	
	@action(detail=True, methods=['post'], serializer_class=FriendSerializer)
	def friend_confirm(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_userprofile.friends_confirmed.clear()

		if "friends_confirmed" in request.POST:
			update_userprofile.add_to_confirmed(request.POST.getlist("friends_confirmed"))

		context = "updated friends_confirmed for user=%s" % update_userprofile.pk
		return HttpResponse(context, status=status.HTTP_200_OK)
