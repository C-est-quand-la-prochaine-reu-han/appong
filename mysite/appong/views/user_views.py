from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from django.db import IntegrityError, connection
from django.core.exceptions import ValidationError

from ..models import UserProfile
from .serializers import UserProfileSerializer, FriendSerializer, AvatarSerializer, RegisterUserSerializer

# TODO cleanup unused headers and comments | debug mode off | .env file for server variables(settings.py.database)


class RegisterUserViewSet(ModelViewSet):
	serializer_class = RegisterUserSerializer
	queryset = UserProfile.objects.all()
	permission_classes = [AllowAny]
	http_method_names = ['post']

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


class UserProfileViewSet(ModelViewSet):
	serializer_class = UserProfileSerializer
	queryset = UserProfile.objects.all()
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def destroy(self, request, pk=None, *args, **kwargs):
		delete_userprofile = UserProfile.objects.filter(pk=request.user.pk)
		if delete_userprofile.count() == 1:
			delete_userprofile[0].anonymise()

		return Response(status=status.HTTP_204_NO_CONTENT)

	@action(detail=False, methods=['get'])
	def me(self, request, *args, **kwargs):
		try:
			instance = UserProfile.objects.get(pk=request.user.pk)
			serializer = self.get_serializer(instance)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)

	@action(detail=False, methods=['put'])
	def update_user(self, request, *args, **kwargs):
		instance = UserProfile.objects.get(pk=request.user.pk)
		serializer = self.get_serializer(instance, data=request.data, partial=True)

		try:
			serializer.is_valid(raise_exception=True)
		except ValidationError as e: #raised by user model validation
			return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)

		try:
			serializer.save()
		except IntegrityError as e: #raised by model constraint name(unique=True)
			return Response(e, status=status.HTTP_400_BAD_REQUEST)

		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	@action(detail=False, methods=['put'], serializer_class=AvatarSerializer, parser_classes = [FileUploadParser])
	def update_avatar(self, request, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(user=request.user.pk)

		if 'file' in request.data:
			update_userprofile.update_avatar(update_userprofile, request.data.get('file'))

		update_userprofile.save()
		context = "updated avatar for user=%s" % update_userprofile.pk
		return Response(context, status=status.HTTP_200_OK)

	@action(detail=False, methods=['post'], serializer_class=FriendSerializer)
	def friends_pending(self, request, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=request.user.pk)
		update_userprofile.friends_pending.clear()

		if "friends_pending" in request.data:
			update_userprofile.add_to_pending(request.data.get("friends_pending"))

		context = "updated friends_pending for user=%s" % update_userprofile.pk
		return Response(context, status=status.HTTP_200_OK)
	
	@action(detail=False, methods=['post'], serializer_class=FriendSerializer)
	def friends_confirm(self, request, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=request.user.pk)
		update_userprofile.friends_confirmed.clear()
		if "friends_confirmed" in request.data:
			update_userprofile.add_to_confirmed(request.data.get("friends_confirmed"))

		context = "updated friends_confirmed for user=%s" % update_userprofile.pk
		return Response(context, status=status.HTTP_200_OK)

	@action(detail=True, methods=['get'])
	def dashboard(self, request, pk, *args, **kwargs):
		try:
			with connection.cursor() as cursor:
				cursor.execute("SELECT * FROM dashboard(%s)", [pk])
				headings = []
				for value in cursor.description:
					headings.append(value.name)
				results_table = dict(zip(headings, cursor.fetchone()))
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)
		return Response(results_table, status=status.HTTP_200_OK)
