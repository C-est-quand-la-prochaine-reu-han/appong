from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	user_nick = models.CharField(max_length=30)
	avatar = models.ImageField(default="default_avatar.jpg")
	friends_confirmed = models.ManyToManyField(blank=True, to="UserProfile", related_name="friend_conf")
	friends_pending = models.ManyToManyField(blank=True, to="UserProfile", related_name="friend_pend")

class Match(models.Model):
	tournament_id = models.ForeignKey(null=True, blank=True, to="Tournament", on_delete=models.CASCADE, related_name="tournament")
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

class Tournament(models.Model):
	tourn_start_time = models.DateTimeField(auto_now_add=True)
	tourn_name = models.CharField(max_length=30)
	tourn_creator = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
	tourn_pending = models.ManyToManyField(blank=True, to="UserProfile", related_name="tourn_pend")
	tourn_confirmed = models.ManyToManyField(blank=True, to="UserProfile", related_name="tourn_conf")
