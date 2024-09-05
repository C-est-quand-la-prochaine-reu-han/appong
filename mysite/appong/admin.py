from django.contrib import admin

from . models import UserProfile, Match, Tournament

class UserAdmin(admin.ModelAdmin):
	filter_horizontal = ('friends')

admin.site.register(UserProfile)
admin.site.register(Match)
admin.site.register(Tournament)
