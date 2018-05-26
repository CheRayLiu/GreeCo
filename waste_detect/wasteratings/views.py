from django.http import HttpResponse
from .models import Rating

def getRatings(request, long, lat, rating):
	newrating = Rating(longitude = float(long), latitude= float(lat), rating = rating)
	newrating.save()
	return HttpResponse(0)