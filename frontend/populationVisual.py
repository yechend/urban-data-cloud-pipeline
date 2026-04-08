import requests
import folium
import logging
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from elasticsearch8 import Elasticsearch

# Set up the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# API url for population data fetched from elastic search
api_url = "http://127.0.0.1:9090/population"
# Fetch the data from API - ElasticSearch
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df_population = pd.DataFrame.from_dict(data, orient='index')
        return df_population
    else:
        print(f"Request failed: {response.status_code}")
        return None
# get the dataframe
df_population=fetch_data(api_url)
# Process the geometry from the GeoJSON file, change it into correct format for Folium map
file_path = "abs_regional_population_summary_sa2_2019-5528703085463955838.json"
def process_geo(file_path):
    # Process the geometry info
    with open(file_path, 'r') as file:
        population_data = json.load(file)
        population_data = population_data['features']
        suburb = list()
        suburb_geo = list()
        for suburb_info in population_data:
            suburb_geo.append(suburb_info["geometry"])
            suburb.append(suburb_info["properties"]["feature_name"])
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    geo_dict = dict(zip(suburb, suburb_geo))
    for suburb_name,geo_info in geo_dict.items():
        feature = {
            "type": "Feature",
            "geometry": geo_info,
            "properties": {
                "name": suburb_name
            },
            "id": suburb_name
        }
        geojson_data["features"].append(feature)
    return geojson_data
geojson_data = process_geo(file_path)
# Process the data we get from elasticsearch
def process_pop(df_population):
    df_population = df_population.fillna(0)
    df_tot = pd.DataFrame({
        'Suburb': df_population['feature_name'],
        'Population': df_population['persons_num']
    })
    df_0_14 = pd.DataFrame({
        'Suburb': df_population['feature_name'],
        'Population': df_population['persons_num'] * df_population['percentage_person_aged_0_14'] / 100
    })
    df_15_64 = pd.DataFrame({
        'Suburb': df_population['feature_name'],
        'Population': df_population['persons_num'] * df_population['percentage_person_aged_15_64'] / 100
    })
    df_65_ = pd.DataFrame({
        'Suburb': df_population['feature_name'],
        'Population': df_population['persons_num'] * df_population['percentage_person_aged_65_plus']/100
    })
    dfs = [df_tot, df_0_14, df_15_64, df_65_]
    return dfs
dfs = process_pop(df_population)

# plot the top 10 suburbs for different age group in dfs with titles
def plot_all_top_suburbs(dfs, titles):
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    for ax, df, title in zip(axs.flat, dfs, titles):
        top_10 = df.sort_values(by='Population', ascending=False).head(10)
        ax.bar(top_10['Suburb'], top_10['Population'], color='lightgreen')
        ax.set_title(title)
        ax.set_xticks(range(len(top_10['Suburb'])))
        ax.set_xticklabels(top_10['Suburb'], rotation=45, ha='right')
        ax.set_xlabel('Suburb')
        ax.set_ylabel('Population')
            
        # Add text labels on top of each bar
        for i, v in enumerate(top_10['Population']):
            ax.text(i, int(v), str(int(v)), ha='center', va='bottom')

    plt.tight_layout()
    plt.show()
    return 

titles = ['Top 10 Suburbs for Total Population', 
            'Top 10 Suburbs for 0-14 Age Group', 
            'Top 10 Suburbs for 15-64 Age Group', 
            'Top 10 Suburbs for 65+ Age Group']
    
# function to call the plotting of bar chart
def bar_chart():
    plot_all_top_suburbs(dfs, titles)
    return

# Plot choropleth plots for each age group in dfs on base map m
def plot_population_map1(m):
    df_list=dfs
    df_name=['Total population','0-14 years old','15-64 years old','above 65 years old']
    df_len = len(df_list)
    folium.TileLayer('openstreetmap', name='Street Map', control=False).add_to(m)
    for i in range(df_len):
        cp=folium.Choropleth(
            geo_data=json.dumps(geojson_data),
            name=df_name[i],
            data=df_list[i],
            columns=["Suburb", "Population"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.5,
            line_opacity=0.2,
            legend_name="total",
            show=False,
            overlay=False,
        ).add_to(m)
        state_data_indexed = df_list[i].set_index('Suburb')

        for s in cp.geojson.data['features']:
            s['properties']['Population'] = int(state_data_indexed.loc[s['id'], 'Population'])
        # Add name and population information for each region on the plot
        folium.GeoJsonTooltip(
            fields=['name', 'Population'],
            aliases=['Suburb', 'Population'],
            localize=True
        ).add_to(cp.geojson)
    folium.LayerControl().add_to(m)
    return m 

