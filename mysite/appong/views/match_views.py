from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes

from django.http import HttpResponse
from ..models import Match, UserProfile
from .serializers import MatchSerializer
from django.core.exceptions import ValidationError

from django.http import HttpResponse

class MatchViewSet(ModelViewSet):
	serializer_class = MatchSerializer
	queryset = Match.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	def delete(self, request, pk, *args, **kwargs):
		Match.objects.get(pk=pk).delete() # ??????????????????
		return HttpResponse("deleted match pk=%s" % pk, status=status.HTTP_204_NO_CONTENT)

	def create(self, request, *args, **kwargs):
		new_match = Match()
		if "player1" not in request.POST \
			or "player2" not in request.POST:
				return HttpResponse("You must provide two players for a match", status=status.HTTP_400_BAD_REQUEST)

		new_match.player1 = UserProfile.objects.get(pk=request.POST.get("player1"))
		new_match.player2 = UserProfile.objects.get(pk=request.POST.get("player2"))
		# TODO add tournament id if in tournament (otherwise default = NULL)
		try:
			new_match.save()
		except ValidationError as e: #error raised in model (see Match.clean: where player1==player2)
			return HttpResponse(e.messages, status=status.HTTP_400_BAD_REQUEST)

		return HttpResponse("created match %s" % new_match.pk, status=status.HTTP_201_CREATED)
