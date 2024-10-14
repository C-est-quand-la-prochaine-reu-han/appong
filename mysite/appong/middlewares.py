from datetime import datetime
from django.utils import timezone
from .models import UserProfile
from django.utils.timezone import make_aware

class UpdateLastAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        response = self.get_response(request)

        try:
            u = UserProfile.objects.get(user__pk=request.user.pk)
            aware_datetime = make_aware(datetime.now())
            u.last_access = datetime.now(tz=aware_datetime.tzinfo)
            u.save()
        except Exception as e:
            pass

        return response
