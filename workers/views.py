from django.shortcuts import render
from django.http import HttpResponse

from .models import Worker

import json

# Helper Function
def condition():
  high_threshold = 0.92
  low_threshold = 0.83
  ctr = Worker.objects.all().count()
  if ctr % 4  == 0:
    condition = high_threshold
    known = True
  elif ctr % 4 == 1:
    condition = low_threshold
    known = True
  elif ctr % 4 == 2:
    condition = high_threshold
    known = False
  else:
    condition = low_threshold
    known = False
  return (condition, known)

# Views
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
    (condition, known) = condition()
    Worker.objects.create(worker_id=worker_id, condition=condition, known=known)
  worker = Worker.objects.get(pk=worker_id)
  return HttpResponse(json.dumps(worker.tojson()))


