from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes

from django.http import HttpResponse
from ..models import Match, UserProfile
from .serializers import MatchSerializer

from django.http import HttpResponse

class MatchViewSet(ModelViewSet):
	serializer_class = MatchSerializer
	queryset = Match.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	def delete(self, request, pk, *args, **kwargs):
		Match.objects.get(pk=pk).delete()
		return HttpResponse("deleted match pk=%s" % pk)

	def create(self, request, *args, **kwargs):
		new_match = Match()
		if "player1" in request.POST == False \
			or "player2" in request.POST == False :
				return HttpResponse("You must provide two players for a match")
		if request.POST.get("player1") == request.POST.get("player2"):
			return HttpResponse("You cannot play against yourself")
		new_match.player1 = UserProfile.objects.get(pk=request.POST.get("player1"))
		new_match.player2 = UserProfile.objects.get(pk=request.POST.get("player2"))
		# TODO add tournament id if in tournament (otherwise default = NULL)
		new_match.save()

		return HttpResponse("created match %s" % new_match.pk)
