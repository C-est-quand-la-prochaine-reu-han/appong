from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from django.http import HttpResponse
from ..models import UserProfile, Tournament
from .serializers import TournamentSerializer, TournamentConfirmedSerializer
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TournamentViewSet(ModelViewSet):
	serializer_class = TournamentSerializer
	queryset = Tournament.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	def delete(self, request, pk, *args, **kwargs):
		Tournament.objects.get(pk=pk).delete()
		context = "deleted tournament pk=%s" % pk
		return HttpResponse(context, status=status.HTTP_204_NO_CONTENT)

	def create(self, request, *args, **kwargs):
		name = request.data.get('tourn_name')
		creator = UserProfile.objects.get(user=request.user)
		pending = request.data.get('tourn_pending')
		if name == '':
			context = "Tournament needs a name"
			return HttpResponse(context, status=status.HTTP_400_BAD_REQUEST)

		try:
			Tournament.objects.create_tournament(name, creator, pending)
		except IntegrityError as e: #raised by model constraint tourn_name(unique=True)
			return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)
		except ValidationError as e:
			return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)

		context = "Tournament %s created" % name
		return HttpResponse(context, status=status.HTTP_201_CREATED)

	@action(detail=True, methods=['post'], serializer_class = TournamentConfirmedSerializer)
	def tourn_confirm(self, request, pk, *args, **kwargs):
		update_tourn = Tournament.objects.get(pk=pk)
		update_tourn.tourn_confirmed.clear()

		if "tour_confirmed" in request.POST:
			update_tourn.add_to_confirmed(request.POST.getlist("tourn_confirmed"))

		context = "updated tourn_confirmed for tournament=%s" % update_tourn.pk
		return HttpResponse(context, status=status.HTTP_200_OK)
