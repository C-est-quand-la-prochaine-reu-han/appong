from rest_framework import serializers, viewsets, permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from django.http import HttpResponse
from ..models import Match

# Serializers define the API representation.

#default user class attributes
class MatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Match
		fields = ['pk', 'tournament_id', 'player1', 'player2', 'match_start_time', 'match_end_time', 'player1_hit_nb', 'player2_hit_nb', 'player1_perfect_hit_nb', 'player2_perfect_hit_nb', 'player1_score', 'player2_score', 'ball_max_speed', 'match_status']

def create(self, data):
	return MatchSerializer.objects.create(**data)

def update(self, instance, data):
	return instance

#model class-based view to only get (list() and retrieve())
class MatchViewSet(ReadOnlyModelViewSet):
	serializer_class = MatchSerializer
	queryset = Match.objects.all()
	permission_classes = [permissions.IsAuthenticated]

	#change name instead of deleting profile
	def delete(self, request, pk, *args, **kwargs):
		return HttpResponse("deleted %s" % pk)
