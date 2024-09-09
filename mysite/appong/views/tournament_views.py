from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes

from django.http import HttpResponse
from ..models import UserProfile, Match, Tournament
from .serializers import TournamentSerializer
from django.db import IntegrityError

from django.http import HttpResponse

class TournamentViewSet(ModelViewSet):
	serializer_class = TournamentSerializer
	queryset = Tournament.objects.all()
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	def delete(self, request, pk, *args, **kwargs):
		Tournament.objects.get(pk=pk).delete()
		return HttpResponse("deleted tournament pk=%s" % pk)
	
	def create(self, request, *args, **kwargs):
		new_tourn = Tournament()
		if request.data.get('tourn_name') == '':
			return HttpResponse("Tournament needs a name")

		new_tourn.tourn_name = request.data.get('tourn_name')
		new_tourn.tourn_creator = UserProfile.objects.get(user=request.user)

		try:
			new_tourn.save()
		except IntegrityError as e: #raised by model constraint tourn_name(unique=True)
			return HttpResponse(e)
		
		for value in request.data.get("tourn_pending"):
			new_tourn.tourn_pending.add(UserProfile.objects.get(pk=value))
		if len(new_tourn.tourn_pending.values_list()) < 3:
			new_tourn.delete()
			return HttpResponse("Tournament needs at least 3 players")

		try:
			new_tourn.save()
		except IntegrityError as e: #not sure what we're catching here
			return HttpResponse(e)

		return HttpResponse("Tournament %s created" % new_tourn.pk)

	@action(detail=True, methods=['post'])
	def tourn_confirm(self, request, pk, *args, **kwargs):
		pass
		# TODO
		# update_userprofile = UserProfile.objects.get(pk=pk)
		# old_friends = update_userprofile.friends_confirmed.values_list()
		# update_userprofile.friends_confirmed.clear()
		# if "friends_confirmed" in request.POST:
		# 	for value in request.POST.getlist("friends_confirmed"):
		# 		friend_confirmed = UserProfile.objects.get(pk=value)
		# 		if update_userprofile.friends_confirmed.contains(friend_confirmed) == False \
		# 			and (update_userprofile.friends_pending.contains(friend_confirmed) \
		# 			or old_friends.contains(friend_confirmed)):
		# 			update_userprofile.friends_confirmed.add(friend_confirmed)
		# 			update_userprofile.friends_pending.remove(friend_confirmed)
		# update_userprofile.save()
		# return HttpResponse("updated friends_confirmed for user=%s" % update_userprofile.pk)

		# return HttpResponse("created tournament %s" % new_tourn.pk)