from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes

from django.http import HttpResponse
from ..models import UserProfile, Match, Tournament
from .serializers import TournamentSerializer, TournamentConfirmedSerializer
from django.db import IntegrityError

from django.http import HttpResponse

class TournamentViewSet(ModelViewSet):
	serializer_class = TournamentSerializer
	queryset = Tournament.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	def delete(self, request, pk, *args, **kwargs):
		Tournament.objects.get(pk=pk).delete()
		return HttpResponse("deleted tournament pk=%s" % pk, status=status.HTTP_204_NO_CONTENT)
	
	def create(self, request, *args, **kwargs):
		new_tourn = Tournament()
		if request.data.get('tourn_name') == '':
			return HttpResponse("Tournament needs a name", status=status.HTTP_400_BAD_REQUEST)

		new_tourn.tourn_name = request.data.get('tourn_name')
		new_tourn.tourn_creator = UserProfile.objects.get(user=request.user)

		try:
			new_tourn.save()
		except IntegrityError as e: #raised by model constraint tourn_name(unique=True)
			return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)
		
		for value in request.data.get("tourn_pending"):
			new_tourn.tourn_pending.add(UserProfile.objects.get(pk=value))
		if len(new_tourn.tourn_pending.values_list()) < 3:
			new_tourn.delete()
			return HttpResponse("Tournament needs at least 3 players", status=status.HTTP_400_BAD_REQUEST)

		try:
			new_tourn.save()
		except IntegrityError as e: #not sure what we're catching here
			return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

		return HttpResponse("Tournament %s created" % new_tourn.pk, status=status.HTTP_201_CREATED)

	@action(detail=True, methods=['post'], serializer_class = TournamentConfirmedSerializer)
	def tourn_confirm(self, request, pk, *args, **kwargs):
		update_tourn = Tournament.objects.get(pk=pk)
		update_tourn.tourn_confirmed.clear()
		for value in request.POST.getlist("tourn_confirmed"):
			friend_confirmed = UserProfile.objects.get(pk=value)
			if update_tourn.tourn_pending.contains(friend_confirmed):
				update_tourn.tourn_confirmed.add(friend_confirmed)
				update_tourn.tourn_pending.remove(friend_confirmed)
		update_tourn.save()
		return HttpResponse("updated tourn_confirmed for tournament=%s" % update_tourn.pk, status=status.HTTP_200_OK)