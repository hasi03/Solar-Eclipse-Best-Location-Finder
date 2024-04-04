import reverse_geocode
from geopy.distance import geodesic
import csv
import pandas as pd
import numpy as np


# Function to get the closest town to a given latitude and longitude
def closest_town(lati, longi):
    location = (lati, longi),
    return reverse_geocode.search(location)



# Find airports within a specified radius (in kilometers) from a given point
def airport_locator(data_path, latitude, longitude, radius_miles=100):
    airports = []
    with open(data_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            airports.append({
                'name': row['name'],
                'type': row['type'],
                'coordinates': (float(row["latitude_deg"]), float(row['longitude_deg']))
            })
    airports = [airport for airport in airports if 'large_airport' in airport['type'] or 'medium_airport' in airport['type']]

    origin = (latitude, longitude)
    nearby_airports = []
    for airport in airports:
        distance_miles  = geodesic(origin, airport['coordinates']).miles
       
        
        if distance_miles <= radius_miles:
            nearby_airports.append((airport['name'], distance_miles, airport['type']))

    nearby_airports = sorted(nearby_airports, key=lambda x: (x[2], x[1])) # Sort by airport type and then by distance

    if not nearby_airports:
        print("No airports found within the specified radius")
        return None
    else:
        df = pd.DataFrame(nearby_airports, columns=['name', 'distance', 'type'])
        return df
