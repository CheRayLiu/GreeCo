from django.db import models
import datetime

class Rating(models.Model):
	date = models.DateTimeField('rating date', default = datetime.now)