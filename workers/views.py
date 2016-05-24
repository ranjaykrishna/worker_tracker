from django.shortcuts import render
from django.http import HttpResponse

from .models import Worker

import json

def index(request):
  window = None
  if 'window' in request.GET:
    window = request.GET['window']
  workers = [w.tojson(window=window) for w in Worker.objects.all()]
  return render(request, 'index.html', {'data': workers})

def workerData(request):
  if 'worker_id' not in request.GET:
    return HttpResponse()
  worker_id = request.GET['worker_id']
  window = 10
  if 'window' in request.GET:
    window = request.GET['window']
  if not Worker.objects.filter(pk=worker_id).exists():
    Worker.objects.create(worker_id=worker_id)
  worker = Worker.objects.get(pk=worker_id)
  return HttpResponse(json.dumps(worker.tojson()))


