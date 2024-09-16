from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from django.contrib.auth.models import User
from ..models import UserProfile
from .serializers import UserProfileSerializer, FriendSerializer

from django.db import IntegrityError
from django.core.exceptions import ValidationError


class UserProfileViewSet(ModelViewSet):
	serializer_class = UserProfileSerializer
	queryset = UserProfile.objects.all()
	authentication_classes = [TokenAuthentication]
	permission_classes = [permissions.IsAuthenticated] # only logged in users can see data
	# permission_classes = [permissions.AllowAny]

	#change name instead of deleting profile from database
	def delete(self, request, pk, *args, **kwargs):
		delete_userprofile = UserProfile.objects.filter(pk=pk)
		if delete_userprofile.count() == 1:
			delete_userprofile[0].anonymise()

		context = "deleted user pk=%s" % pk
		return Response(context, status=status.HTTP_204_NO_CONTENT)

	def create(self, request, *args, **kwargs): # reinvented the wheel here

		serializer = self.get_serializer(data=request.data)
		try:
			serializer.is_valid(raise_exception=True)
		except ValidationError as e: #raised by user model validation
			return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)

		try:
			serializer.save()
		except IntegrityError as e: #raised by model constraint (unique=True)
			return Response(e, status=status.HTTP_400_BAD_REQUEST)
		
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def update(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_user_nick = request.data.get("user_nick")
		update_userprofile.user_nick = update_user_nick
		if "avatar" in request.FILES:
			update_userprofile.update_avatar(update_userprofile, request.FILES["avatar"])

		try:
			update_userprofile.save()
		except IntegrityError as e: #raised by model constraint name(unique=True)
			return Response(e, status=status.HTTP_400_BAD_REQUEST)

		context = "updated user pk=%s" % update_userprofile.pk
		return Response(context, status=status.HTTP_200_OK)

	@action(detail=True, methods=['post'], serializer_class=FriendSerializer)
	def friends_pending(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_userprofile.friends_pending.clear()

		if "friends_pending" in request.data:
			update_userprofile.add_to_pending(request.data.get("friends_pending"))

		context = "updated friends_pending for user=%s" % update_userprofile.pk
		return Response(context, status=status.HTTP_200_OK)
	
	@action(detail=True, methods=['post'], serializer_class=FriendSerializer)
	def friends_confirm(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_userprofile.friends_confirmed.clear()
		if "friends_confirmed" in request.data:
			update_userprofile.add_to_confirmed(request.data.get("friends_confirmed"))

		context = "updated friends_confirmed for user=%s" % update_userprofile.pk
		return Response(context, status=status.HTTP_200_OK)
