from datetime import datetime
from .models import UserProfile

class UpdateLastAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            u = UserProfile.objects.get(user__pk=request.user.pk)
            u.last_access = datetime.now()
            u.save()
        except:
            pass

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
