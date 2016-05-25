from django.core.management.base import BaseCommand
from workers.models import *
from workers.utils import *

import time

class Command(BaseCommand):
  def handle(self, *args, **options):
    hit_dict = {}
    for hit in Hit.objects.all():
      if hit.assignment_id in hit_dict:
        hit.delete()
      hit_dict[hit.assignment_id] = 1
