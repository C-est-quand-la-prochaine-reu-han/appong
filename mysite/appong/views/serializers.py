from rest_framework import serializers
from rest_framework.serializers import PrimaryKeyRelatedField, ModelSerializer

from django.contrib.auth.models import User
from ..models import UserProfile, Friend

# Serializers define the API representation.
class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ['username']

# class FriendSerializer(serializers.ModelSerializer):
# 	user1 = serializers.PrimaryKeyRelatedField(source="friend.user1", queryset=UserProfile.objects.all())
# 	user2 = serializers.PrimaryKeyRelatedField(source="friend.user2", queryset=UserProfile.objects.all())
# 	status = serializers.IntegerField(source="friend.status")
# 	class Meta:
# 		model = Friend
# 		fields = ['user1', 'user2', 'status']

class FriendSerializer(PrimaryKeyRelatedField, ModelSerializer):
	class Meta:
		model = Friend
		fields = ['user1', 'user2','status']

# class StatusSerializer(PrimaryKeyRelatedField, ModelSerializer):
# 	class Meta:
# 		model = Friend
# 		fields = ['status']

class UserProfileSerializer(ModelSerializer):
	user = UserSerializer(required=True)
	friends = FriendSerializer(required=True, many=True, queryset=UserProfile.objects.all())

	class Meta:
		model = UserProfile
		fields = ['pk', 'user', 'user_nick', 'avatar', 'friends']