from rest_framework import serializers

from django.contrib.auth.models import User
from ..models import UserProfile, Friend

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']

class FriendSerializer(serializers.ModelSerializer):
	class Meta:
		model = Friend
		fields = ['user1', 'user2', 'status']

class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(required=True)
	friends = FriendSerializer(required=True)

	class Meta:
		model = UserProfile
		fields = ['pk', 'user', 'user_nick', 'avatar', 'friends']