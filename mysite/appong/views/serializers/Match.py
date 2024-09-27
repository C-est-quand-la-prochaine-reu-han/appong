from rest_framework import serializers
from ...models import Match, Tournament
from django.core.exceptions import ValidationError

class MatchSerializer(serializers.ModelSerializer):
	def validate(self, data):
		if data.get("player1") == data.get("player2"):
			raise ValidationError("Player can't play against themselves")
		return data

	class Meta:
		model = Match
		fields =	['pk',
					'tournament', 
					'player1', 'player2', 
					'match_start_time', 'match_end_time', 
					'player1_hit_nb', 'player2_hit_nb', 
					'player1_perfect_hit_nb', 'player2_perfect_hit_nb', 
					'player1_score', 'player2_score', 
					'ball_max_speed', 
					'match_status']

