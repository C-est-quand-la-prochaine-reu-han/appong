from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ...models import UserProfile
import django.contrib.auth.password_validation as validators

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'password']
		extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(required=True)
	class Meta:
		model = UserProfile
		read_only_fields = ['pk', 'friends_pending', 'friends_confirmed']
		fields =	['pk', 'user', 'user_nick', 'avatar',
					'friends_pending', 'friends_confirmed']

class FriendSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields =	['friends_pending', 'friends_confirmed']