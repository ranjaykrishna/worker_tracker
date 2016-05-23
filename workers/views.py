from django.shortcuts import render
from django.http import HttpResponse

from .models import Worker

import json

def index(request):
  workers = [w.tojson() for w in Worker.objects.all()]
  return render(request, 'index.html', {'data': json.dumps(workers)})

def workerData(request):
  if 'worker_id' not in request.GET:
    return HttpResponse()
  worker_id = request.GET['worker_id']
  if not Worker.objects.filter(pk=worker_id).exists():
    Worker.objects.create(worker_id=worker_id)
  worker = Worker.objects.get(pk=worker_id)
  return HttpResponse(json.dumps(worker.tojson()))


