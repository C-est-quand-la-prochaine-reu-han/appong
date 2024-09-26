from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile	


class UserProfileManager(models.Manager):
	def create_userprofile(self, user, user_nick, avatar=None):
		new_user = User.objects.create(username=user.get('username'))
		new_user.set_password(user.get('password'))

		new_userprofile = UserProfile()
		new_userprofile.user = new_user
		new_userprofile.user_nick = user_nick
		# if avatar is not None:
		# 	new_userprofile.update_avatar(new_userprofile, avatar)

		new_user.save()
		new_userprofile.save()
		return new_userprofile


class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	user_nick = models.CharField(max_length=30, unique=True)
	avatar = models.ImageField(default="default_avatar.jpg")
	friends_pending = models.ManyToManyField('self', blank=True, symmetrical=True)
	friends_confirmed = models.ManyToManyField('self', blank=True, symmetrical=True)

	objects = UserProfileManager()

	def resize_image(self, image):
		try:
			img = Image.open(image)
			imagename = image.name
		except:
			imagename = "media/default_avatar.jpg"
			img = Image.open(imagename)
		# Resize the image to a desired size (e.g., 300x300)
		resized_img = img.resize((300, 300), resample=Image.BICUBIC)

		# Convert the resized image to bytes
		buffer = BytesIO()
		resized_img.save(buffer, format='png')
		img_bytes = buffer.getvalue()
		img.close()
		
		return (img_bytes, imagename)

	def update_avatar(self, user, file):
		image, file = self.resize_image(file)
		user.avatar.save(file, ContentFile(image), save=False)

	def add_to_pending(self, new_friends):
		friend_pending = UserProfile.objects. \
			filter(pk__in=new_friends). \
			exclude(pk__in=self.friends_confirmed.all()). \
			exclude(pk=self.pk)
		self.friends_pending.add(*friend_pending)

	def add_to_confirmed(self, new_friends):
		friend_confirmed = UserProfile.objects. \
			filter(pk__in=new_friends). \
			filter(Q(pk__in=self.friends_confirmed.all()) | Q(pk__in=self.friends_pending.all()))
		self.friends_confirmed.add(*friend_confirmed)
		self.friends_pending.remove(*friend_confirmed)

	def anonymise(self):
		user_object = User.objects.get(pk=self.user.pk)
		user_object.username = "deleted" + str(self.pk)
		user_object.is_active = False

		self.user_nick = "deaded" + str(self.pk)
		self.avatar = "default_avatar.jpg"
		self.friends_pending.clear()
		self.friends_confirmed.clear()

		user_object.save()
		self.save()

	def __str__(self):
		return self.user.username
