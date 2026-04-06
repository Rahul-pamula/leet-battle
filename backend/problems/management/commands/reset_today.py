from datetime import date
from django.core.management.base import BaseCommand
from problems.models import DailyAssignment


class Command(BaseCommand):
    help = "Delete today's DailyAssignment rows (dev utility)"

    def handle(self, *args, **options):
        today = date.today()
        qs = DailyAssignment.objects.filter(assigned_date=today)
        count = qs.count()
        qs.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} assignments for {today}"))
