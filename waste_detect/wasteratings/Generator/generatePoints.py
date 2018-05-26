from wasteratings.models import Rating
from datetime import datetime,timedelta
import random
from django.utils import timezone

def points():

	longhi, longlo, lathi, latlo = -79.313432,-79.437372 ,43.752594,43.634184
	dlong = longhi -longlo
	dlat =	lathi - latlo

	for day in range(100):
		for i in range(100):
			lat = latlo + random.random()*dlat
			long = longlo + random.random()*dlong
			rating = round(max(1, min(random.gauss(day/20 + 1 , 0.75), 5)))

			newrating = Rating(longitude = long, latitude= lat, rating = rating, date = timezone.now()-timedelta(days=100-day))
			newrating.save()



points()	

