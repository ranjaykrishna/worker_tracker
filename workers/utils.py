from workers.models import *
from boto.mturk.connection import MTurkConnection

def get_mturk_connection_from_args():
  args = json.load(open('config.json'))
  return MTurkConnection('mechanicalturk.amazonaws.com', **args)

def approve(hit, attention_score=None, condition=None):
  mtc = get_mturk_connection_from_args()
  if score is None:
    message = 'Good job. You passed all the attention checks.'
  else:
    message = 'You did not get all the attention checks. But your current score is %d\%. So you are still doing well. It\'s impossible to get all the attention checks. As long as you stay above the threshold of %d\%, you have nothing to worry about.' % (attention_score, condition)
  mtc.approve_assignment(hit.assignment_id, message)

def reject(hit, attention_score=None, condition=None):
  mtc = get_mturk_connection_from_args()
  message = 'You failed the attention checks.'
  if score != None:
    message += ' Your current score of %d\% dropped below the acceptance rate of %d\%.' % (attention_score, condition)
  mtc.reject_assignment(hit.assignment_id, message)

def processHit():
  WINDOW = 10
  hits = Hit.objects.filter(processed=False)
  for hit in hits:
    old_hits = Hit.objects.filter(worker=hit.worker, processed=True).order_by('-pk')[:WINDOW]
    if float(hit.num_pos_golds_correct + hit.num_neg_golds_correct)/(hit.num_pos_golds + hit.num_neg_golds) == 1.0:
      approve(hit)
    elif old_hits.count() < WINDOW:
      approve(hit)
    else:
      num_correct = 0.0
      total = 0.0
      for old_hit in old_hits:
        num_correct += old_hit.num_pos_golds_correct
        num_correct += old_hit.num_neg_golds_correct
        total += old_hit.num_pos_golds
        total += old_hit.num_neg_golds
      score = 0.0
      if total > 0.0:
        score = 100.0*num_correct/total
      if score > hit.worker.condition:
        approve(hit, attention_score=int(score), condition=hit.worker.condition)
      else:
        reject(hit, attention_score=int(score), condition=hit.worker.condition)
    hit.processed = True
    hit.save()
