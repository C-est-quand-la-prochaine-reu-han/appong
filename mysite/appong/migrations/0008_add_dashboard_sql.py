# Generated by Django 5.1 on 2024-09-12 12:14

from django.db import migrations, models

SQL = "CREATE OR REPLACE FUNCTION dashboard(pk BIGINT)\
			RETURNS TABLE(\
				match_played FLOAT, \
				match_wins FLOAT, \
				total_hits FLOAT, \
				perfect_hits FLOAT, \
				total_score FLOAT, \
				fastest_ball FLOAT, \
				win_ratio FLOAT, \
				perfect_hit_ratio FLOAT)\
			LANGUAGE plpgsql\
			AS $$\
			BEGIN\
				match_played := (SELECT(SELECT CAST(COUNT(*) AS Float) FROM appong_match WHERE player1_id=pk OR player2_id=pk) AS match_played);\
				match_wins := (SELECT CAST(COUNT(*) AS Float) FROM appong_match WHERE (player1_id=pk AND player1_score > player2_score) OR (player2_id=pk AND player2_score > player1_score));\
				total_hits := (SELECT ((SELECT CAST(COALESCE(SUM(player1_hit_nb), 0) AS Float) FROM appong_match WHERE player1_id=pk) + (SELECT COALESCE(SUM(player2_hit_nb), 0) FROM appong_match WHERE player2_id=pk)));\
				perfect_hits := (SELECT ((SELECT CAST(COALESCE(SUM(player1_perfect_hit_nb), 0) AS Float) FROM appong_match WHERE player1_id=pk) + (SELECT COALESCE(SUM(player2_perfect_hit_nb), 0) FROM appong_match WHERE player2_id=pk)));\
				total_score := (SELECT ((SELECT CAST(COALESCE(SUM(player1_score), 0) AS Float) FROM appong_match WHERE player1_id=pk) + (SELECT COALESCE(SUM(player2_score), 0) FROM appong_match WHERE player2_id=pk)));\
				fastest_ball := (SELECT COALESCE(MAX (ball_max_speed),0) FROM appong_match WHERE player1_id=pk OR player2_id=pk);\
				win_ratio := match_wins/match_played;\
				perfect_hit_ratio := perfect_hits/total_hits;\
			RETURN next;\
			END;\
			$$;"

class Migration(migrations.Migration):

    dependencies = [
        ('appong', '0007_rename_tourn_creator_tournament_creator_and_more'),
    ]

    operations = [migrations.RunSQL(SQL)]