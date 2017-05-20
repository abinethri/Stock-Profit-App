from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class StockValues(models.Model):
	date = models.DateTimeField(
            default=timezone.now)
	name = models.CharField(max_length=300)
	ticker = models.CharField(max_length=300)
	price = models.FloatField()
