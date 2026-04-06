from django.core.management.base import BaseCommand
from problems.models import Problem
from problems.seed_data.week1 import WEEK_1_PROBLEMS

class Command(BaseCommand):
    help = 'Seed the database with week 1 problems'

    def handle(self, *args, **options):
        for pdata in WEEK_1_PROBLEMS:
            Problem.objects.get_or_create(
                slug=pdata['slug'],
                defaults=pdata
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(WEEK_1_PROBLEMS)} problems.'))
