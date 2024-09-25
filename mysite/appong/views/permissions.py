from rest_framework import permissions

from django.contrib.auth.models import User
from ..models import UserProfile


class IsAdminOwnerOrReadOnly(permissions.BasePermission):
	# def has_permission(self, request, view): #checks user is authenticated
	# 	if request.user.is_authenticated:
	# 		return True

	def has_object_permission(self, request, view, obj):
		print ("-----", obj)
		print ("-----", request.user)
		if request.user.is_superuser: #allows admin to do everything
			return True
		if request.method in permissions.SAFE_METHODS: #allows SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
			return True
		if type(obj) == User: #checks user is author of object (and that object is user)
			return obj == request.user
		if type(obj) == UserProfile: #checks user is author of object (and that object is userprofile)
			return obj.user == request.user
		return False