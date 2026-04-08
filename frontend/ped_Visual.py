import DateTime
from DateTime import timedelta
import folium
import folium.plugins as plugins
from folium import Marker
import pandas as pd
import requests
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
import folium
import matplotlib.pyplot as plt

def plot_hourly_pedestrian_count(df):
    # Ensure the 'timestamp' column is of datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # If the 'timestamp' column does not have timezone information, set it to UTC
    if df['timestamp'].dt.tz is None:
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')

    # Convert the 'timestamp' column to 'Australia/Melbourne' timezone
    df['timestamp'] = df['timestamp'].dt.tz_convert('Australia/Melbourne')

    # Extract the hour from the 'timestamp' column
    df['hour'] = df['timestamp'].dt.hour

    # Group by hour and aggregate 'total_of_directions' to get sum and mean
    hourly_summary = df.groupby('hour')['total_of_directions'].agg(['sum', 'mean']).reset_index()

    # Plotting the mean pedestrian count by hour
    plt.figure(figsize=(10, 6))
    bars = plt.bar(hourly_summary['hour'], hourly_summary['mean'], color='skyblue')

    # Add text labels on the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2 - 0.1, yval + 0.1, round(yval, 2), ha='center', va='bottom', fontsize=6)

    # Set the labels and title of the plot
    plt.xlabel('Hour of the Day')
    plt.ylabel('Mean of Pedestrian Counting')
    plt.title('Mean of Pedestrian Counting by Hour of the Day')
    plt.xticks(hourly_summary['hour'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def plot_mean_pedestrian_by_sensor(df):
    
    # Ensure the 'timestamp' column is of datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # If the 'timestamp' column does not have timezone information, set it to UTC
    if df['timestamp'].dt.tz is None:
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')
    
    # Extract the date from the 'timestamp' column
    df['date'] = df['timestamp'].dt.date

    # Group by sensor name and aggregate 'total_of_directions' and 'date'
    sensor_summary = df.groupby('sensor_name').agg({'total_of_directions': 'sum', 'date': 'nunique'}).reset_index()

    # Calculate mean per day
    sensor_summary['mean_per_day'] = sensor_summary['total_of_directions'] / sensor_summary['date']

    # Sort the summary by mean per day in descending order
    sensor_summary = sensor_summary.sort_values(by='mean_per_day', ascending=False)

    # Plotting the mean pedestrian count per day by sensor name
    plt.figure(figsize=(15, 6))
    bars = plt.bar(sensor_summary['sensor_name'], sensor_summary['mean_per_day'], color='skyblue', width=0.5)

    # Set the labels and title of the plot
    plt.xlabel('Sensor Name')
    plt.ylabel('Mean of Pedestrian Counting per Day')
    plt.title('Mean of Pedestrian Counting per Day by Sensor Name')
    plt.xticks(rotation=90)  # Rotate x-axis labels to avoid overlap
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()  # Adjust layout to fit labels
    plt.xlim(-0.5, len(sensor_summary['sensor_name']) - 0.5)
    plt.show()

def create_sensor_map(file_path, map_object):
    ## Read the JSON file into a DataFrame
    df_locations = pd.read_json(file_path)

    # Add markers for each sensor location
    for _, row in df_locations.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Sensor: {row['sensor_name']}",
            tooltip=row['sensor_name']
        ).add_to(map_object)
    #folium.LayerControl().add_to(m)

def create_sensor_map1(file_path,m):
    # Read the JSON file into a DataFrame
    df_locations = pd.read_json(file_path)

    # Create a map centered around the average latitude and longitude
    #m = folium.Map(location=[df_locations['latitude'].mean(), df_locations['longitude'].mean()], zoom_start=14)

    # Add markers for each sensor location
    for _, row in df_locations.iterrows():
        fg = folium.FeatureGroup(name=row['sensor_name'])
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Sensor: {row['sensor_name']}",
            tooltip=row['sensor_name']
        ).add_to(fg)
        fg.add_to(m)

    # Add layer control to the map
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m.save('sensors_map.html')

    return m

def create_pedcount_map(data,df,m):
    if df['timestamp'].dt.tz is None:
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')
    earliest_timestamp = df['timestamp'].min()
    time_index = [
     (earliest_timestamp + k * timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S") for k in range(len(data))
    ]

    #m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=14)
    hm = folium.plugins.HeatMapWithTime(data, index=time_index, auto_play=True, max_opacity=0.5,min_opacity=0.1)
    hm.add_to(m)
    folium.LayerControl().add_to(m)
    return m

