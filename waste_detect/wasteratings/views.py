from django.http import HttpResponse
from .models import Rating
from datetime import datetime, timedelta
import json 
import numpy as np

# Insert a new ratings into the database at the given location
def newrating(request, long, lat, rating):
	newrating = Rating(longitude = float(long), latitude= float(lat), rating = rating)
	newrating.save()
	return HttpResponse(0)

# List all the ratings within a given area
def viewratings(request, longlo, longhi, latlo, lathi):
	ratings = Rating.objects.filter(longitude__range=(longlo,longhi), latitude__range=(latlo,lathi))
	response = ""
	for rating in ratings:
		response += str(rating.rating) + "<br>"
	return HttpResponse(response)

# Map ratings based on longitude, latitude and date range in days
def mapratings(request, longlo, longhi, latlo, lathi, timeframe):
	longlo = float(longlo)
	longhi = float(longhi)
	latlo = float(latlo)
	lathi = float(lathi)
	steps = 10
	#loop from left to right and up to down, creating equally spaced points with the right weights (average of the points in that box)



	dlong = (longhi - longlo) / steps
	dlat = (lathi - latlo) / steps

	long =[]
	lat =[]
	avgrate =[]


	longrange = np.arange(longlo,longhi,dlong).tolist()
	latrange = np.arange(latlo,lathi ,dlat).tolist()

	for x in longrange:
		for y in latrange:
			ratings = Rating.objects.filter(longitude__range=(x,x+dlong)						#filter by longitude range
									, latitude__range=(y,y+dlat)							#filter by latitude range
									, date__lte = datetime.now() - timedelta(days=timeframe)	#timeframe selected by user (days) -- lte means less than or equal to
									)
			sum =0;
			for rating in ratings:
				sum+=rating.rating
			if ratings.count() == 0:
				avg = 0
			else:
				avg = float(sum) /ratings.count()
			long += [x+dlong/2]
			lat += [y+dlat/2]
			avgrate+=[avg]

	response = {'long': long, 'lat': lat, 'wt': avgrate}

	responsestr = json.dumps(response)

	return HttpResponse(responsestr)