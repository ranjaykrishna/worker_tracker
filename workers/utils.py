from workers.models import *
from boto.mturk.connection import MTurkConnection

import json
import os, sys

def get_mturk_connection_from_args():
  if os.path.exists('config.json'):
    args = json.load(open('config.json'))
  else:
    args = {'aws_access_key': os.environ['aws_access_key'], 'aws_secret_key': os.environ['aws_secret_key']}
  #return MTurkConnection(host='mechanicalturk.sandbox.amazonaws.com', aws_access_key_id=args['aws_access_key'], aws_secret_access_key= args['aws_secret_key'])
  return MTurkConnection(host='mechanicalturk.amazonaws.com', aws_access_key_id=args['aws_access_key'], aws_secret_access_key= args['aws_access_key'])

def approve(hit, message):
  mtc = get_mturk_connection_from_args()
  try:
    mtc.approve_assignment(hit.assignment_id, message)
    print hit.assignment_id, message
    hit.processed = True
    hit.save()
  except:
    print "Failed to Approve: %s, %s" % (hit.assignment_id, message)

def reject(hit, message):
  mtc = get_mturk_connection_from_args()
  try:
    mtc.reject_assignment(hit.assignment_id, message)
    print hit.assignment_id, message
    hit.processed = True
    hit.save()
  except:
    print "Failed to Reject: %s, %s" % (hit.assignment_id, message)

def processHits():
  WINDOW = 10
  hits = Hit.objects.filter(processed=False)
  for hit in hits:
    old_hits = Hit.objects.filter(worker=hit.worker, pk__lt=hit.pk).order_by('-pk')[:WINDOW]
    old_hits_to_process = []
    if hit.num_pos_golds_correct + hit.num_neg_golds_correct == hit.num_pos_golds + hit.num_neg_golds:
      message = 'Good job. You passed all the attention checks.'
      approve(hit, message)
    elif old_hits.count() < WINDOW:
      continue
    else:
      num_correct = 0.0
      total = 0.0
      for old_hit in old_hits:
        if not old_hit.processed:
          old_hits_to_process.append(old_hit)
        num_correct += old_hit.num_pos_golds_correct
        num_correct += old_hit.num_neg_golds_correct
        total += old_hit.num_pos_golds
        total += old_hit.num_neg_golds
      score = 0.0
      if total > 0.0:
        score = 100.0*num_correct/total
      if score > hit.worker.condition:
        message = ('You did not get all the attention checks but your current score is %d%% correct. You are still doing well. It\'s impossible to get all the attention checks. As long as you stay above the threshold of %d%%, you have nothing to worry about.' % (int(score), hit.worker.condition))
        approve(hit, message)
        for ohtp in old_hits_to_process:
          approve(ohtp, message)
      else:
        message = 'You did not pass the attention checks. Your current score of %d%% is below the acceptance rate of %d%%.' % (int(score), hit.worker.condition)
        reject(hit, message)
        for ohtp in old_hits_to_process:
          reject(ohtp, message)
