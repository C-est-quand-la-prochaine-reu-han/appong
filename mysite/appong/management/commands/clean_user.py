from django.core.management.base import BaseCommand, CommandError
from ...models import UserProfile
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        aware_datetime = make_aware(datetime.now())
        date_cutoff = datetime.now(tz=aware_datetime.tzinfo) - timedelta(days=365)
        # date_cutoff = datetime.now(tz=aware_datetime.tzinfo) - timedelta(seconds=30)

        users_past_cutoff = UserProfile.objects.filter(last_access__lt=date_cutoff)
        for user in users_past_cutoff:
            user.anonymise()   