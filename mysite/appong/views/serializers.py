from rest_framework import serializers

from django.contrib.auth.models import User
from ..models import UserProfile, Match, Tournament

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']

class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(required=True)

	class Meta:
		model = UserProfile
		fields =	['pk', 'user', 'user_nick', 'avatar',\
					'friends_pending', 'friends_confirmed']

class MatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Match
		fields =	['tournament_id', \
					'player1', 'player2', \
					'match_start_time', 'match_end_time', \
					'player1_hit_nb', 'player2_hit_nb', \
					'player1_perfect_hit_nb', 'player2_perfect_hit_nb', \
					'player1_score', 'player2_score', \
					'ball_max_speed', 'match_status']