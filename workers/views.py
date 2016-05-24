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

def process(data):
  hit = {'num_pos_golds': 0, 'num_pos_golds_correct': 0,
      'num_neg_golds': 0, 'num_neg_golds_correct': 0}
  gold = json.load(open('gold_dict.json'))

  def key(i):
    return str(i['image_id']) + '_' + i['text'] + '_' + str(i['bbox']['x']) + '_' + str(i['bbox']['y'])

  for i in data:
    k = key(i)
    if k not in gold:
      continue
    elif gold[k] == 1:
      hit['num_pos_golds'] += 1
      if i['vote']:
        hit['num_pos_golds_correct'] += 1
    elif gold[k] == -1:
      hit['num_neg_golds'] += 1
      if not i['vote']:
        hit['num_neg_golds_correct'] += 1
  return hit

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

def hitData(request):
  if request.method != 'POST':
    return HttpResponse({})
  data = json.loads(request.POST['data'])
  worker_id = data['worker_id']
  if not Worker.objects.filter(pk=worker_id).exists():
    return HttpResponse({})
  hit = process(data['output'])
  Hit.objects.create(hit_id='',
    worker=worker,
    num_pos_golds = hit['num_pos_golds'],
    num_neg_golds = hit['num_neg_golds'],
    num_pos_golds_correct = hit['num_pos_golds_correct'],
    num_neg_golds_correct = hit['num_neg_golds_correct']
  )
  return HttpResponse({})
