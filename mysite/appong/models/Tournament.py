from django.db import models, IntegrityError
from .UserProfile import UserProfile


class TournamentManager(models.Manager):
	def create_tournament(self, name, creator, pending):
		new_tournament = Tournament()
		new_tournament.tourn_name = name
		new_tournament.tourn_creator = creator

		new_tournament.save()

		pending_list = UserProfile.objects.filter(id__in=pending)
		new_tournament.tourn_pending.add(*pending_list)
		if new_tournament.tourn_pending.count() < 3:
			new_tournament.delete()
			raise IntegrityError("Tournament needs at least 3 players")


class Tournament(models.Model):
	tourn_start_time = models.DateTimeField(auto_now_add=True)
	tourn_name = models.CharField(max_length=30, unique=True)
	tourn_creator = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
	tourn_pending = models.ManyToManyField(blank=True, to="UserProfile", related_name="tourn_pend")
	tourn_confirmed = models.ManyToManyField(blank=True, to="UserProfile", related_name="tourn_conf")

	objects = TournamentManager()

	def __str__(self):
		return self.tourn_name
	
	def add_to_confirmed(self, new_players):
		players = UserProfile.objects. \
			filter(pk__in=new_players). \
			filter(pk__in=self.tourn_pending)
		self.tourn_confirmed.add(*players)
		self.tourn_pending.remove(*players)
