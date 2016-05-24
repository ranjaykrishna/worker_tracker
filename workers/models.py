from django.db import models

class Worker(models.Model):
  worker_id = models.SlugField(max_length=128, primary_key=True)
  condition = models.PositiveIntegerField(default=0)
  known = models.BooleanField(default=False)

  def tojson(self, window=None):
    if window == None:
      hits = Hit.objects.filter(worker__pk=self.pk)
    else:
      hits = Hit.objects.filter(worker__pk=self.pk).order_by('-pk')[:window]
    num_pos_golds = 0
    num_pos_golds_correct = 0
    num_neg_golds = 0
    num_neg_golds_correct = 0
    for hit in hits:
      num_pos_golds += hit.num_pos_golds
      num_pos_golds_correct += hit.num_pos_golds_correct
      num_neg_golds += hit.num_neg_golds
      num_neg_golds_correct += hit.num_neg_golds_correct
    return {'worker_id': self.worker_id,
      'condition': self.condition,
      'known': self.known,
      'num_pos_golds': num_pos_golds,
      'num_neg_golds': num_neg_golds,
      'num_pos_golds_correct': num_pos_golds_correct,
      'num_neg_golds_correct': num_neg_golds_correct,
      'num_hits': hits.count()}

class Hit(models.Model):
  hit_id = models.SlugField(max_length=128)
  assignment_id = models.SlugField(max_length=128)
  processed = models.BooleanField(default=False)
  worker = models.ForeignKey(Worker)
  num_pos_golds = models.PositiveIntegerField(default=0)
  num_neg_golds = models.PositiveIntegerField(default=0)
  num_pos_golds_correct = models.PositiveIntegerField(default=0)
  num_neg_golds_correct = models.PositiveIntegerField(default=0)
  approved = models.NullBooleanField(default=None)

  def __str__(self):
    return "assignment_id: %s, pos: %d/%d, neg: %d/%d, approved: %s" % (
        self.assignment_id,
        self.num_pos_golds_correct,
        self.num_pos_golds,
        self.num_neg_golds_correct,
        self.num_neg_golds,
        str(self.approved))
