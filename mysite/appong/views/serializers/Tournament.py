from rest_framework import serializers
from ...models import Tournament
from .UserProfile import UserProfileSerializer
from django.core.exceptions import ValidationError

class TournamentSerializer(serializers.ModelSerializer):
	tourn_creator = UserProfileSerializer(read_only=True)
	class Meta:
		model = Tournament
		read_only_fields = ['tourn_confirmed']
		fields =	['pk', 
					'tourn_name', 
					'tourn_creator', 
					'tourn_pending', 
					'tourn_confirmed']

class TournamentMatchSerializer(serializers.ModelSerializer):
	pk = serializers.PrimaryKeyRelatedField(required=True, queryset=Tournament.objects.all())
	class Meta:
		model = Tournament
		fields =	['pk']

class TournamentConfirmedSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields =	['tourn_confirmed']
