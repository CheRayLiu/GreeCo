from django.http import HttpResponse
from .models import Rating

def getRatings(request):
	return HttpResponse("Hello")