import random

from django.db import transaction
from django.core.management.base import BaseCommand

from ...models import Image
from ...factory import (
    ImageFactory
)

NUM_Images = 100

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Image]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        # Add some images
        for _ in range(NUM_Images):
            image = ImageFactory()
          