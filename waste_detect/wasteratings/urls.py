from django.urls import path

from . import views

urlpatterns = [
    path('rate/<str:long>/<str:lat>/<int:rating>', views.getRatings, name='Rate it'),
]