from django.urls import path

from . import views

urlpatterns = [
    path('rate/', views.newrating, name='Rate it'),
    path('<str:longlo>/<str:longhi>/<str:latlo>/<str:lathi>', views.viewratings, name='List ratings in area'),
    path('map/', views.mapratings, name='Generate map of ratings in area'),
]