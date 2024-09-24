from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from django.contrib.auth.models import User
from ..models import UserProfile
from .serializers import UserProfileSerializer, FriendSerializer, MatchSerializer

from django.db import IntegrityError, connection
from django.core.exceptions import ValidationError


class UserProfileViewSet(ModelViewSet):
	serializer_class = UserProfileSerializer
	queryset = UserProfile.objects.all()
	authentication_classes = [TokenAuthentication]
	# permission_classes = [permissions.IsAuthenticated] # only logged in users can see data
	permission_classes = [permissions.AllowAny]

	#change name instead of deleting profile from database
	def delete(self, request, pk, *args, **kwargs):
		delete_userprofile = UserProfile.objects.filter(pk=pk)
		if delete_userprofile.count() == 1:
			delete_userprofile[0].anonymise()

		context = "deleted user pk=%s" % pk
		return Response(context, status=status.HTTP_204_NO_CONTENT)

	def create(self, request, *args, **kwargs): # reinvented the wheel here

		serializer = self.get_serializer(data=request.data)
		try:
			serializer.is_valid(raise_exception=True)
		except ValidationError as e: #raised by user model validation
			return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)

		try:
			serializer.save()
		except IntegrityError as e: #raised by model constraint (unique=True)
			return Response(e, status=status.HTTP_400_BAD_REQUEST)
		
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def update(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_user_nick = request.data.get("user_nick")
		update_userprofile.user_nick = update_user_nick
		if "avatar" in request.FILES:
			update_userprofile.update_avatar(update_userprofile, request.FILES["avatar"])

		try:
			update_userprofile.save()
		except IntegrityError as e: #raised by model constraint name(unique=True)
			return Response(e, status=status.HTTP_400_BAD_REQUEST)

		context = "updated user pk=%s" % update_userprofile.pk
		return Response(context, status=status.HTTP_200_OK)

	@action(detail=True, methods=['post'], serializer_class=FriendSerializer)
	def friends_pending(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_userprofile.friends_pending.clear()

		if "friends_pending" in request.data:
			update_userprofile.add_to_pending(request.data.get("friends_pending"))

		context = "updated friends_pending for user=%s" % update_userprofile.pk
		return Response(context, status=status.HTTP_200_OK)
	
	@action(detail=True, methods=['post'], serializer_class=FriendSerializer)
	def friends_confirm(self, request, pk, *args, **kwargs):
		update_userprofile = UserProfile.objects.get(pk=pk)
		update_userprofile.friends_confirmed.clear()
		if "friends_confirmed" in request.data:
			update_userprofile.add_to_confirmed(request.data.get("friends_confirmed"))

		context = "updated friends_confirmed for user=%s" % update_userprofile.pk
		return Response(context, status=status.HTTP_200_OK)

	@action(detail=True, methods=['get'], serializer_class=MatchSerializer)
	def dashboard(self, request, pk, *args, **kwargs):
		with connection.cursor() as cursor:
			cursor.execute("CREATE OR REPLACE FUNCTION dashboard(pk BIGINT)\
				RETURNS FLOAT[]\
				LANGUAGE plpgsql\
				AS $$\
				DECLARE \
					match_played FLOAT;\
					match_wins FLOAT;\
					total_hits FLOAT;\
					perfect_hits FLOAT;\
					total_score FLOAT;\
					fastest_ball FLOAT;\
					win_ratio FLOAT;\
					perfect_hit_ratio FLOAT;\
				BEGIN\
					match_played := (SELECT CAST(COUNT(*) AS Float) FROM appong_match WHERE player1_id=pk OR player2_id=pk);\
					match_wins := (SELECT CAST(COUNT(*) AS Float) FROM appong_match WHERE (player1_id=pk AND player1_score > player2_score) OR (player2_id=pk AND player2_score > player1_score));\
					total_hits := (SELECT ((SELECT CAST(COALESCE(SUM(player1_hit_nb), 0) AS Float) FROM appong_match WHERE player1_id=pk) + (SELECT COALESCE(SUM(player2_hit_nb), 0) FROM appong_match WHERE player2_id=pk)));\
					perfect_hits := (SELECT ((SELECT CAST(COALESCE(SUM(player1_perfect_hit_nb), 0) AS Float) FROM appong_match WHERE player1_id=pk) + (SELECT COALESCE(SUM(player2_perfect_hit_nb), 0) FROM appong_match WHERE player2_id=pk)));\
					total_score := (SELECT ((SELECT CAST(COALESCE(SUM(player1_score), 0) AS Float) FROM appong_match WHERE player1_id=pk) + (SELECT COALESCE(SUM(player2_score), 0) FROM appong_match WHERE player2_id=pk)));\
					fastest_ball := (SELECT COALESCE(MAX (ball_max_speed),0) FROM appong_match WHERE player1_id=pk OR player2_id=pk);\
					win_ratio = match_wins/match_played;\
					perfect_hit_ratio = perfect_hits/total_hits;\
				RETURN array[match_played::FLOAT, match_wins::FLOAT, total_hits::FLOAT, perfect_hits::FLOAT, total_score::FLOAT, fastest_ball::FLOAT, win_ratio::FLOAT, perfect_hit_ratio::FLOAT];\
				END;\
				$$;")
			cursor.execute("SELECT dashboard(%s)", [pk])
			row = cursor.fetchone()

		print("-----", row)
		return Response(row, status=status.HTTP_200_OK)
