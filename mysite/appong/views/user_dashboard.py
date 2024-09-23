from django.contrib.auth.models import User
from ..models import UserProfile

from django.db import connection

from rest_framework import viewsets, permissions
from rest_framework.response import Response

# The object django.db.connection represents the default database connection. 
# To use the database connection, call connection.cursor() to get a cursor object.
# Then, call cursor.execute(sql, [params]) to execute the SQL 
# and cursor.fetchone() or cursor.fetchall() to return the resulting rows.

	# SELECT - extracts data from a database
	# COUNT

class UserDashboard(viewsets.ViewSet):
	queryset = UserProfile.objects.all()
	permission_classes = [permissions.IsAuthenticated]

	def retrieve(self, request, pk=None):
		with connection.cursor() as cursor:
			cursor.execute("SELECT COUNT(*) FROM appong_match WHERE player1_id = %s OR player2_id = %s", [pk])
			row = cursor.fetchone()

		print("-----", row)
		return Response(row) # see dictfetchall() 
	

# number of wins
# win rate (wins/number of matches played)
# number of perfect hits
# proportion of perfect hits (perfect/hit number)
# average game score
# fastest ball

# number of tournament wins
# total gaming Time

#number of matches played
#SELECT COUNT(*) FROM appong_match WHERE player1_id=1 OR player2_id=1

#number of wins
#SELECT COUNT(*) FROM appong_match WHERE (player1_id=1 AND player1_score > player2_score) OR (player2_id=1 AND player2_score > player1_score)

#number of perfect hits
#SELECT COALESCE(SUM(player1_perfect_hit_nb), 0) FROM appong_match WHERE player1_id=1
# + 
#SELECT COALESCE(SUM(player2_perfect_hit_nb), 0) FROM appong_match WHERE player2_id=1

#number of hits
#SELECT SUM (player1_hit_nb) FROM appong_match WHERE player1_id=1
# +
#SELECT SUM (player2_hit_nb) FROM appong_match WHERE player2_id=1

#total score
#SELECT SUM (player1_score) FROM appong_match WHERE player1_id=1
# +
#SELECT SUM (player2_score) FROM appong_match WHERE player2_id=1

#fastest ball in a game they played
#SELECT MAX (ball_max_speed) FROM appong_match WHERE player1_id=1 OR player2_id=1

# When SUM finds no matches, returns NULL, not 0
# Can use TOTAL instead (returns floating point)
# OR IFNULL condition (not sure of syntax)
# OR COALESCE
# SELECT COALESCE(SUM(player2_score), 0) FROM appong_match WHERE player2_id=1

#SELECT(SELECT TOTAL (player1_score) FROM appong_match WHERE player1_id=1) + (SELECT TOTAL (playe
# GROUPBY
# COUNT IN FLOATS
