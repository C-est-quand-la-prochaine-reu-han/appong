from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from django.db import IntegrityError
from django.core.exceptions import ValidationError

from ..models import Match
from .serializers import MatchSerializer


class MatchViewSet(ModelViewSet):
	serializer_class = MatchSerializer
	queryset = Match.objects.all()
	permission_classes = [permissions.IsAuthenticated] # Only logged in users can see data

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			serializer.is_valid(raise_exception=True)
		except ValidationError as e:
			return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)

		try:
			serializer.save()
		except IntegrityError as e:
			return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
