from rest_framework import serializers
from ...models import Match, Tournament
from .Tournament import TournamentMatchSerializer

class MatchSerializer(serializers.ModelSerializer):
	tournament_id = TournamentMatchSerializer(required=False)

	class Meta:
		model = Match
		fields =	['tournament_id', 
					'player1', 'player2', 
					'match_start_time', 'match_end_time', 
					'player1_hit_nb', 'player2_hit_nb', 
					'player1_perfect_hit_nb', 'player2_perfect_hit_nb', 
					'player1_score', 'player2_score', 
					'ball_max_speed', 
					'match_status']
