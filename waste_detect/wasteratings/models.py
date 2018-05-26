from django.db import models
from datetime import datetime

class Rating(models.Model):
	date = models.DateTimeField('rating date', default = datetime.now)
	rating = models.PositiveSmallIntegerField('rating')
	longitude = models.FloatField('longitude')
	latitude = models.FloatField('latitude')