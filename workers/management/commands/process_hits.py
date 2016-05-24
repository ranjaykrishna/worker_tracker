from django.core.management.base import BaseCommand
from workers.models import *
from workers.utils import *

import time

class Command(BaseCommand):
  def handle(self, *args, **options):
    while True:
      processHits()
      time.sleep(5)
