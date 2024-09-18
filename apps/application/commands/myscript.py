from django.core.management.base import BaseCommand
from apps.application.models import Application  # Import your models here

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Your code here
        print(Application.objects.all())
