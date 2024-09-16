from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet

from django.http import HttpResponse
from ..models import Match, UserProfile, Tournament
from .serializers import MatchSerializer
from django.db import IntegrityError

from django.core.exceptions import ValidationError
from rest_framework.response import Response

class MatchViewSet(ModelViewSet):
	serializer_class = MatchSerializer
	queryset = Match.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			serializer.is_valid(raise_exception=True)
		except ValidationError as e:
			return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)

		try:
			serializer.save()
		except IntegrityError as e:
			return Response(e.message, status=status.HTTP_400_BAD_REQUEST)

		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
