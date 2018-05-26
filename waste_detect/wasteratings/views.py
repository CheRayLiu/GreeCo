from django.http import HttpResponse
from .models import Rating
from datetime import datetime, timedelta

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
def mapratings(request, longlo, longhi, latlo, lathi, timelo, timehi):
	ratings = Rating.objects.filter(longitude__range=(longlo,longhi)
									, latitude__range=(latlo,lathi)
									, date__gte = datetime.now() - timedelta(days=timelo)
									, date__lt = datetime.now() - timedelta(days=timehi)
									)
	steps = 10
	#loop from left to right and up to down, creating equally spaced points with the right weights (average of the points in that box)
	response = "" # return JSON string containing latitude / longitude of points, and their weights (for the Google Maps API)
	for rating in ratings:
		response += str(rating.rating) + "<br>"
	return HttpResponse(response)