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
  return MTurkConnection(host='mechanicalturk.amazonaws.com', aws_access_key_id=args['aws_access_key'], aws_secret_access_key= args['aws_secret_key'])

def approve(mtc, hit, message):
  try:
    mtc.approve_assignment(hit.assignment_id, message)
    print hit.assignment_id, message
    hit.processed = True
    hit.approved = True
    hit.save()
  except Exception, e:
    print "Failed to Approve: %s, %s" % (hit.assignment_id, message)

def reject(mtc, hit, message):
  try:
    mtc.reject_assignment(hit.assignment_id, message)
    print hit.assignment_id, message
    hit.processed = True
    hit.approved = False
    hit.save()
  except:
    print "Failed to Reject: %s, %s" % (hit.assignment_id, message)

def processHits():
  WINDOW = 10
  hits = Hit.objects.filter(processed=False)
  mtc = get_mturk_connection_from_args()
  for hit in hits:
    old_hits = Hit.objects.filter(worker=hit.worker, pk__lt=hit.pk).order_by('-pk')[:WINDOW-1]
    old_hits_to_process = []
    if hit.num_pos_golds_correct + hit.num_neg_golds_correct == hit.num_pos_golds + hit.num_neg_golds:
      message = 'Good job. Keep going!'
      if hit.worker.known:
        message = 'Good job. You passed all the attention checks.'
      approve(mtc, hit, message)
    elif old_hits.count() < WINDOW-1:
      continue
    else:
      num_correct = hit.num_pos_golds_correct + hit.num_neg_golds_correct
      total = hit.num_pos_golds + hit.num_neg_golds
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
        message = 'Good job. Keep going!'
        if hit.worker.known:
          message = ('You did not get all the attention checks but your current score is %d%% correct. You are still doing well. It\'s impossible to get all the attention checks. As long as you stay above the threshold of %d%%, you have nothing to worry about.' % (int(score), hit.worker.condition))
        approve(mtc, hit, message)
        for ohtp in old_hits_to_process:
          approve(mtc, ohtp, message)
      else:
        message = 'You are not performing well on the attention checks.'
        if hit.worker.known:
          message = 'You did not pass the attention checks. Your current score of %d%% is below the acceptance rate of %d%%.' % (int(score), hit.worker.condition)
        reject(mtc, hit, message)
        for ohtp in old_hits_to_process:
          reject(mtc, ohtp, message)
  mtc.close()
