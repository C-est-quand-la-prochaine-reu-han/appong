from rest_framework import serializers, viewsets, permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from django.http import HttpResponse
from django.contrib.auth.models import User
from ..models import UserProfile

# Serializers define the API representation.

#default user class attributes
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(required=True)

	class Meta:
		model = UserProfile
		fields = ['pk', 'user', 'user_nick', 'avatar']


## ViewSets define the view behavior.
#class UserViewSet(viewsets.ModelViewSet):
#	queryset = UserProfile.objects.all().order_by('-user__date_joined')
#	serializer_class = UserProfileSerializer
#	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data


def create(self, data):
	return UserProfile.objects.create(**data)

def update(self, instance, data):
	instance.user_nick = data.get('user_nick', instance.user_nick)
	instance.avatar = data.get('avatar', instance.avatar)
	instance.save()
	return instance

#model class-based view to only get (list() and retrieve())
class UserProfileViewSet(ReadOnlyModelViewSet):
	serializer_class = UserProfileSerializer
	queryset = UserProfile.objects.all().order_by('-user__date_joined')
	permission_classes = [permissions.IsAuthenticated]#only logged in users can see data

	#change name instead of deleting profile
	def delete(self, request, pk, *args, **kwargs):
		instance = UserProfile.objects.get(pk=pk)
		instance.user.username = "deleted" + pk
		instance.user_nick = "deaded" + pk
		instance.user.is_active = False
		instance.avatar = "default_avatar.jpg"
		instance.save()
		#UserProfile.objects.get(pk=pk).delete()
		return HttpResponse("deleted %s" % pk)
