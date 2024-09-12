from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet

from django.http import HttpResponse
from ..models import Match, UserProfile, Tournament
from .serializers import MatchSerializer
from django.core.exceptions import ValidationError

class MatchViewSet(ModelViewSet):
	serializer_class = MatchSerializer
	queryset = Match.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	def delete(self, request, pk, *args, **kwargs):
		Match.objects.get(pk=pk).delete()
		context = "deleted match pk=%s" % pk
		return HttpResponse(context, status=status.HTTP_204_NO_CONTENT)

	def create(self, request, *args, **kwargs):
		new_match = Match()
		if "player1" not in request.data \
			or "player2" not in request.data:
				context = "You must provide two players for a match"
				return HttpResponse(context, status=status.HTTP_400_BAD_REQUEST)

		new_match.player1 = UserProfile.objects.get(pk=request.data.get("player1"))
		new_match.player2 = UserProfile.objects.get(pk=request.data.get("player2"))
		print(request.data)
		if 'tournament.tourn_name' in request.data:
			new_match.tournament = Tournament.objects.get(pk=request.data.get("tournament.tourn_name"))
		try:
			new_match.save()
		except ValidationError as e: #error raised in model (see Match.clean: where player1==player2)
			return HttpResponse(e.messages, status=status.HTTP_400_BAD_REQUEST)

		context = "created match %s" % new_match.pk
		return HttpResponse(context, status=status.HTTP_201_CREATED)
