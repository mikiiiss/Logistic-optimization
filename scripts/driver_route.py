import pandas as pd
import folium
from geopy.distance import geodesic

# Load the dataset
data = pd.read_csv('order_with_trip_info.csv')

data['order_id'].nunique()

# Split 'trip_origin' into separate latitude and longitude columns
data[['origin_lat', 'origin_lng']] = data['trip_origin'].str.strip('"').str.split(',', expand=True).astype(float)

# Check for missing values in the relevant columns
missing_data = data[['lat', 'lng', 'origin_lat', 'origin_lng']].isnull().sum()
print("Missing values in columns:\n", missing_data)

# Drop rows with missing values in the relevant columns
data = data.dropna(subset=['lat', 'lng', 'origin_lat', 'origin_lng'])

# Filter the data for the specific order_id
order_id = 392001
specific_order_data = data[data['order_id'] == order_id]

if specific_order_data.empty:
    print(f"No data found for order_id {order_id}")
else:
    # Function to calculate the distance
    def calculate_distance(row):
        start = (row['lat'], row['lng'])
        end = (row['origin_lat'], row['origin_lng'])
        return geodesic(start, end).kilometers

    # Calculate distance for the specific order
    specific_order_data['distance_to_origin'] = specific_order_data.apply(calculate_distance, axis=1)
    print(specific_order_data[['lat', 'lng', 'origin_lat', 'origin_lng', 'distance_to_origin']])

    # Create a map centered around the specific order's origin
    map_center = [specific_order_data['lat'].mean(), specific_order_data['lng'].mean()]
    mymap = folium.Map(location=map_center, zoom_start=12)

    # Function to add a route to the map
    def add_route(row):
        start = [row['lat'], row['lng']]
        end = [row['origin_lat'], row['origin_lng']]
        folium.Marker(location=start, popup='Start').add_to(mymap)
        folium.Marker(location=end, popup='Origin').add_to(mymap)
        folium.PolyLine([start, end], color='blue').add_to(mymap)

    # Apply the function to the specific order row
    specific_order_data.apply(add_route, axis=1)

    # Save the map to an HTML file
    file_path = 'specific_order_route_map.html'
    mymap.save(file_path)

# Function to calculate the distance for all data
def calculate_distance(row):
    start = (row['lat'], row['lng'])
    end = (row['origin_lat'], row['origin_lng'])
    return geodesic(start, end).kilometers

# Apply the function to calculate distances for all data
data['distance_to_origin'] = data.apply(calculate_distance, axis=1)
print(data[['lat', 'lng', 'origin_lat', 'origin_lng', 'distance_to_origin']])

# Create a map centered around the first point
map_center = [data['lat'].mean(), data['lng'].mean()]
mymap = folium.Map(location=map_center, zoom_start=12)

# Function to add a route to the map
def add_route(row):
    start = [row['lat'], row['lng']]
    end = [row['origin_lat'], row['origin_lng']]
    folium.Marker(location=start, popup='Start').add_to(mymap)
    folium.Marker(location=end, popup='Origin').add_to(mymap)
    folium.PolyLine([start, end], color='blue').add_to(mymap)

# Apply the function to each row in the DataFrame
data.apply(add_route, axis=1)

# Save the map to an HTML file
mymap.save('routes_map.html')