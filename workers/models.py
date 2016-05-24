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
    num_pos_gold = 0
    num_pos_gold_correct = 0
    num_neg_gold = 0
    num_neg_gold_correct = 0
    for hit in hits:
      num_pos_gold += hit.num_pos_gold
      num_pos_gold_correct += hit.num_pos_gold_correct
      num_neg_gold += hit.num_neg_gold
      num_neg_gold_correct += hit.num_neg_gold_correct
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
  worker = models.ForeignKey(Worker)
  num_pos_golds = models.PositiveIntegerField(default=0)
  num_neg_golds = models.PositiveIntegerField(default=0)
  num_pos_golds_correct = models.PositiveIntegerField(default=0)
  num_neg_golds_correct = models.PositiveIntegerField(default=0)

