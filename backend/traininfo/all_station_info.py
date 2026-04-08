from elasticsearch8 import Elasticsearch
import json


def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()


# Connect to Elasticsearch
# Get Elasticsearch username and password from environment variables

es_username = config('ES_USERNAME')
es_password = config('ES_PASSWORD')

# Connect to Elasticsearch
client = Elasticsearch(
    'https://elasticsearch-master.elastic.svc.cluster.local:9200',
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=(es_username, es_password)  # Use environment variables
)

# query the location information of all the stations
query_station_geo = {
    "query": {
        "match_all": {}
    },
    "size": 500
}

# query all station service count
query_service_count = {
    "size": 0,
    "aggs": {
        "station": {
            "terms": {"field": 'Station_Name', "size": 500}
        }
    }
}


def main():
    # retrieve data about station
    response_station_geo = client.search(
        index="station_position",
        body=query_station_geo
    )
    station_info = dict()
    station_geo = response_station_geo["hits"]["hits"]
    for geo in station_geo:
        key = geo['_source']['Station_Name']
        station_info[key] = {
            'Station_Latitude': geo['_source']['Station_Latitude'],
            'Station_Longitude': geo['_source']['Station_Longitude']
        }
    # retrieve count info from another index
    res = client.search(index='train_service_passenger_counts_2022_2023', body=query_service_count)
    count_info = res['aggregations']['station']["buckets"]
    for bucket in count_info:
        station_info[bucket["key"]]["count"] = bucket["doc_count"]

    return json.dumps(station_info)
