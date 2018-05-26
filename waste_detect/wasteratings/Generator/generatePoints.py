from wasteratings.models import Rating
from datetime import datetime,timedelta
import random
def points():

	longlo, longhi, latlo, lathi = -79.437372,-79.313432,43.634184, 43.752594
	dlong = longhi -longlo
	dlat =	lathi - latlo

	for day in range(100):
		for i in range(100):
			lat = latlo + random.random()*dlat
			long = longlo + random.random()*dlong
			rating = round(max(1, min(random.gauss(day/20 + 1 , 0.75), 5)))

			newrating = Rating(longitude = long, latitude= lat, rating = rating, date = datetime.now()-timedelta(days=100-day))
			newrating.save()



points()	

