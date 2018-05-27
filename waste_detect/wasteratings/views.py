from django.http import HttpResponse
from .models import Rating
from datetime import datetime, timedelta
import json

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
	
	#loop from left to right and up to down, creating equally spaced points with the right weights (average of the points in that box)



	

	long =[]
	lat =[]
	avgrate =[]


	date = datetime.now(timezone.utc) - timedelta(days=body['slideJ'])

	
	ratings = Rating.objects.filter(longitude__range=(longlo,longhi)						#filter by longitude range
									, latitude__range=(latlo,lathi)							#filter by latitude range
									, date__range = (date - timedelta(days=days), date)	#timeframe selected by user (days) -- lte means less than or equal to
									)[:points]
	
	for rating in ratings:
		long += [rating.longitude]
		lat += [rating.latitude]
		avgrate+=[rating.rating]

	

	response = {'long': long, 'lat': lat, 'wt': avgrate}

	responsestr = json.dumps(response)

	return HttpResponse(responsestr)