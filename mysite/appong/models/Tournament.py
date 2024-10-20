from django.db import models, IntegrityError
from datetime import datetime

from .UserProfile import UserProfile


class TournamentManager(models.Manager):
	def create_tournament(self, start_time, name, creator, pending):
		new_tournament = Tournament()
		new_tournament.start_time = start_time
		new_tournament.name = name
		new_tournament.creator = creator

		new_tournament.save()

		pending_list = UserProfile.objects.filter(id__in=pending)
		new_tournament.pending.add(*pending_list)
		if new_tournament.pending.count() < 3:
			new_tournament.delete()
			raise IntegrityError("Tournament needs at least 3 players")


class Tournament(models.Model):
	start_time = models.DateTimeField(auto_now_add=datetime.now)
	name = models.CharField(max_length=30, unique=True)
	creator = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True)
	pending = models.ManyToManyField(blank=True, to="UserProfile", related_name="pend")
	confirmed = models.ManyToManyField(blank=True, to="UserProfile", related_name="conf")

	objects = TournamentManager()

	def __str__(self):
		return self.name
	
	def add_to_confirmed(self, new_players):
		players = UserProfile.objects. \
			filter(pk__in=new_players). \
			filter(pk__in=self.pending.all())
		self.confirmed.add(*players)
		self.pending.remove(*players)
