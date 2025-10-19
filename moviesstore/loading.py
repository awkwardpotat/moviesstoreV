import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviesstore.settings')  # Change to your project name!
django.setup()

from map.models import WorldBorder

# Clear existing data
WorldBorder.objects.all().delete()
print("Cleared existing data")

# Load YOUR GeoJSON file
with open('map/data/TM_WORLD_BORDERS-0.3.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Import each country
for feature in data['features']:
    props = feature['properties']
    geometry = feature['geometry']
    
    WorldBorder.objects.create(
        fips=props.get('FIPS'),
        iso2=props.get('ISO2'),
        iso3=props.get('ISO3'),
        un=props.get('UN'),
        name=props.get('NAME'),
        area=props.get('AREA'),
        pop2005=props.get('POP2005'),
        region=props.get('REGION'),
        subregion=props.get('SUBREGION'),
        lon=props.get('LON'),
        lat=props.get('LAT'),
        mpoly_json=json.dumps(geometry)  # Use mpoly_json (your actual field name)
    )
    print(f"Imported {props.get('NAME')}")

print(f"\nDone! Imported {WorldBorder.objects.count()} countries")