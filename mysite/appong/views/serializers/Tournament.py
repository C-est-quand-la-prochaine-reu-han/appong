from rest_framework import serializers
from ...models import Tournament, UserProfile
from .UserProfile import UserProfileSerializer
from django.core.exceptions import ValidationError

class TournamentSerializer(serializers.ModelSerializer):
	creator = UserProfileSerializer(read_only=True)

	def validate_pending(self, pending):
		if len(list(dict.fromkeys(pending))) < 3:
			raise ValidationError("tournament requires at least 3 players")
		return pending

	class Meta:
		model = Tournament
		read_only_fields = ['start_time',
					  'confirmed']
		fields =	['pk', 
					'name', 
					'creator', 
					'pending', 
					'confirmed']


class TournamentConfirmedSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tournament
		fields =	['confirmed']
