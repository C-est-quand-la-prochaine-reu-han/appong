from rest_framework import serializers
from ...models import Tournament
from .UserProfile import UserProfileSerializer
from django.core.exceptions import ValidationError

class TournamentSerializer(serializers.ModelSerializer):
	creator = UserProfileSerializer(read_only=True)
	class Meta:
		model = Tournament
		read_only_fields = ['confirmed']
		fields =	['pk', 
					'name', 
					'creator', 
					'pending', 
					'confirmed']

class TournamentMatchSerializer(serializers.ModelSerializer):
	name = serializers.PrimaryKeyRelatedField(required=False, queryset=Tournament.objects.all())
	class Meta:
		model = Tournament
		fields =	['pk', 'name']

class TournamentConfirmedSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields =	['confirmed']
