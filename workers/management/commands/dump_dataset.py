from django.core.management.base import BaseCommand
from workers.models import *
from workers.utils import *

import json

class Command(BaseCommand):
  def handle(self, *args, **options):
    hits = []
    for hit in Hit.objects.all():
      hits.append(hit.tojson())
    print json.dumps(hits)

