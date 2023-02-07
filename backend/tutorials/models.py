from django.db import models

class Tutorial(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField(blank=False, default='')
    answer = models.TextField(blank=False, default='')