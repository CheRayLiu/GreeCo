from django.http import HttpResponse
from .models import Rating
from datetime import datetime, timedelta, timezone
import json
import numpy as np

# Insert a new ratings into the database at the given location
def newrating(request):
	jsonstring = request.body
	jsondict = json.loads(jsonstring)
	newrating = Rating(longitude = jsondict["long"], latitude= jsondict["lat"], rating = jsondict["rating"])
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
def mapratings(request):
	
	rbody =request.body
	body = json.loads(rbody)
	longlo = body['longloJ']
	longhi = body['longhiJ']
	latlo = body['latloJ']
	lathi = body['lathiJ']
	steps = 10
	#loop from left to right and up to down, creating equally spaced points with the right weights (average of the points in that box)



	dlong = (longhi - longlo) / steps
	dlat = (lathi - latlo) / steps

	long =[]
	lat =[]
	avgrate =[]
	points = 100	# take maximum this many points per box
	days = 90 		# consider points this up to this many days before the slider


	longrange = np.arange(longlo,longhi,dlong).tolist()
	latrange = np.arange(latlo,lathi ,dlat).tolist()

	date = datetime.now(timezone.utc) - timedelta(days=body['slideJ'])

	for x in longrange:
		for y in latrange:
			ratings = Rating.objects.filter(longitude__range=(x,x+dlong)						#filter by longitude range
									, latitude__range=(y,y+dlat)							#filter by latitude range
									, date__range = (date - timedelta(days=days), date)	#timeframe selected by user (days) -- lte means less than or equal to
									)[:points]
			sum = 0.0
			totalWeight = 0.0
			for rating in ratings:
				timeDiff = date - rating.date
				weight = sqrt(-(timeDiff.days) + days)	# weight function
				totalWeight += weight
				sum+=rating.rating * weight
			if ratings.count() == 0:
				avg = 0
			else:
				avg = float(sum) / totalWeight
			long += [x+dlong/2]
			lat += [y+dlat/2]
			avgrate+=[avg]

	response = {'long': long, 'lat': lat, 'wt': avgrate}

	responsestr = json.dumps(response)

	return HttpResponse(responsestr)