from django.contrib import admin

from . models import UserProfile, Match, Tournament

admin.site.register(UserProfile)
admin.site.register(Match)
admin.site.register(Tournament)
