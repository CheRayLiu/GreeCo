from django.urls import path

from . import views

urlpatterns = [
    path('rate/<str:long>/<str:lat>/<int:rating>', views.newrating, name='Rate it'),
    path('<str:longlo>/<str:longhi>/<str:latlo>/<str:lathi>', views.viewratings, name='View ratings in area'),
]