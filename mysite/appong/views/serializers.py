from rest_framework import serializers

from django.contrib.auth.models import User
from ..models import UserProfile

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']

class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(required=True)

	class Meta:
		model = UserProfile
		fields = ['pk', 'user', 'user_nick', 'avatar', 'friends_pending', 'friends_confirmed']