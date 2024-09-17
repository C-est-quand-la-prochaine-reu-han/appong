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
		read_only_fields = ['pk', 'friends_pending', 'friends_confirmed', 'avatar']
		fields =	['pk', 'user', 'user_nick', 'avatar',
					'friends_pending', 'friends_confirmed']

	def create(self, validated_data):
		return UserProfile.objects.create_userprofile(**validated_data)

	def update(self, instance, validated_data):
		if "user" in validated_data:
			if "username" in validated_data.get("user"):
				instance.user.username = validated_data.get("user").get("username")
			if "password" in validated_data.get("user"):
				instance.user.set_password(validated_data.get("user").get("password"))
		if "user_nick" in validated_data:
			instance.user_nick = (validated_data.get("user_nick"))
		instance.user.save()
		instance.save()
		return instance

class FriendSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields =	['friends_pending', 'friends_confirmed']

class AvatarSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields =	['avatar']
