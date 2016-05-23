from django.db import models

class Worker(models.Model):
  worker_id = models.SlugField(max_length=128, primary_key=True)
  condition = models.PositiveIntegerField(default=0)
  known = models.BooleanField(default=False)
  num_pos_golds = models.PositiveIntegerField(default=0)
  num_neg_golds = models.PositiveIntegerField(default=0)
  num_pos_golds_correct = models.PositiveIntegerField(default=0)
  num_neg_golds_correct = models.PositiveIntegerField(default=0)
  num_hits = models.PositiveIntegerField(default=0)

  def tojson(self):
    return {'worker_id': self.worker_id,
      'condition': self.condition,
      'known': self.known,
      'num_pos_golds': self.num_pos_golds,
      'num_neg_golds': self.num_neg_golds,
      'num_pos_golds_correct': self.num_pos_golds_correct,
      'num_neg_golds_correct': self.num_neg_golds_correct,
      'num_hits': self.num_hits}
