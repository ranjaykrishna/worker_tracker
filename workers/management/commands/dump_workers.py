from django.core.management.base import BaseCommand
from workers.models import *

import json

class Command(BaseCommand):
  def handle(self, *args, **options):
    for worker in Worker.objects.all():
      print json.dumps(worker.tojson())

