from django.db import models
from django.core.exceptions import ValidationError
from .UserProfile import UserProfile

#TODO need to change match time defaults as game as saved only at end
#Use match status to declare the end of a tournament

class Match(models.Model):
	tournament = models.ForeignKey(null=True, blank=True, to="Tournament", on_delete=models.CASCADE, related_name="tournament")
	player1 = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name="player1")
	player2 = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name="player2")
	match_start_time = models.DateTimeField(auto_now_add=True)
	match_end_time = models.DateTimeField(auto_now=True)
	player1_hit_nb = models.PositiveIntegerField(default=0)
	player2_hit_nb = models.PositiveIntegerField(default=0)
	player1_perfect_hit_nb = models.PositiveIntegerField(default=0)
	player2_perfect_hit_nb = models.PositiveIntegerField(default=0)
	player1_score = models.PositiveIntegerField(default=0)
	player2_score = models.PositiveIntegerField(default=0)
	ball_max_speed = models.PositiveIntegerField(default=0)
	match_status = models.PositiveIntegerField(default=0)

	def clean(self):
		if self.player1 == self.player2:
			raise ValidationError("Users can't play against themselves")

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return str(self.pk)
