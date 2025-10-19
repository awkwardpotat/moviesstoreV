from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse
from .models import WorldBorder
from movies.models import Movie
import json

# Page view — just returns the HTML
def world_map(request):
    return render(request, "map/map.html")

# Data view — returns GeoJSON
def world_data(request):
    borders = WorldBorder.objects.all()

    features = []
    for border in borders:
        top_movies = get_top_movies_for_country(border.name, limit=2)  # Get top 2

        feature = {
            "type": "Feature",
            "properties": {
                "name": border.name,
                "top_movies": top_movies  # Changed from top_movie to top_movies
            },
            "geometry": json.loads(border.mpoly_json)
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    return JsonResponse(json.dumps(geojson_data), safe=False)
# def world_data(request):
#     borders = WorldBorder.objects.all()

#     features = []
#     for border in borders:
#         top_movie = get_top_movie_for_country(border.name)

#         feature = {
#             "type": "Feature",
#             "properties": {
#                 "name": border.name,
#                 "top_movie": {
#                     'name': top_movie['name'],
#                     'image': top_movie['image'],
#                     'views': top_movie['views'],
#                     'orders': top_movie['orders']
#                 } if top_movie else None
#             },
#             "geometry": json.loads(border.mpoly_json)
#         }
#         features.append(feature)

#     geojson_data = {
#         "type": "FeatureCollection",
#         "features": features
#     }

#     return JsonResponse(json.dumps(geojson_data), safe=False)

def get_top_movies_for_country(country_name, limit=2):
    """Get the top N most popular movies for a specific country (by orders, then views)"""
    movies = Movie.objects.all()

    movie_stats = []

    for movie in movies:
        orders = movie.orders_by_region.get(country_name, 0)
        views = movie.views_by_region.get(country_name, 0)

        if orders > 0 or views > 0:  # Only include movies with activity
            movie_stats.append({
                'name': movie.name,
                'image': movie.image.url if movie.image else '',
                'views': views,
                'orders': orders
            })

    # Sort by orders (descending), then by views (descending)
    movie_stats.sort(key=lambda x: (x['orders'], x['views']), reverse=True)

    # Return top N movies
    return movie_stats[:limit]

# def get_top_movie_for_country(country_name):
#     """Get the most popular movie for a specific country (by orders, then views)"""
#     movies = Movie.objects.all()

#     top_movie = None
#     max_orders = 0
#     max_views = 0

#     for movie in movies:
#         orders = movie.orders_by_region.get(country_name, 0)
#         views = movie.views_by_region.get(country_name, 0)

#         # Check if this movie is better than current top
#         if orders > max_orders or (orders == max_orders and views > max_views):
#             max_orders = orders
#             max_views = views
#             top_movie = {
#                 'name': movie.name,
#                 'image': movie.image.url if movie.image else '',
#                 'views': views,
#                 'orders': orders
#             }

#     return top_movie