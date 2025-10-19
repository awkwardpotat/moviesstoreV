from django.urls import path
from . import views

urlpatterns = [
    path("", views.world_map, name="map.world_map"),
    path("map/data/", views.world_data, name="map.world_data"),
]