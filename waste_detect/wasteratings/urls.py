from django.urls import path

from . import views

urlpatterns = [
    path('rate/<str:long>/<str:lat>/<int:rating>', views.newrating, name='Rate it'),
    path('<str:longlo>/<str:longhi>/<str:latlo>/<str:lathi>', views.viewratings, name='List ratings in area'),
    path('map/<str:longlo>/<str:longhi>/<str:latlo>/<str:lathi>/<int:timeframe>', views.mapratings, name='Generate map of ratings in area'),
]