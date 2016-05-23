from django.shortcuts import render
from django.http import HttpResponse

from .models import Worker

import json

def index(request):
  workers = [w.tojson() for w in Worker.objects.all()]
  return render(request, 'index.html', {'data': json.dumps(workers)})

