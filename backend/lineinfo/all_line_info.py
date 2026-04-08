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

# query the line information of all the stations
query_line_geo = {
    "query": {
        "match_all": {}
    },
    "size": 500
}

# query the line count in the largest dataset
query_line_service_count = {
    "size": 0,
    "aggs": {
        "line": {
            "terms": {"field": 'Line_Name', "size": 500}
        }
    }
}


def main():
    # retrieve data about lines
    response_line_info = client.search(
        index="transport_line_information",
        body=query_line_geo
    )
    line_info = dict()

    for line in response_line_info["hits"]["hits"]:
        line_name = line['_source']['Line_Name']
        line_info[line_name] = {
            'Mode': line['_source']['Line_Mode'],
            'Group': line['_source']['Group'],
            'Stations_Number': line['_source']['Stations_Number']
        }
        line_station = list()
        line_geo = list()
        for key, value in line['_source']['Stations'].items():
            line_station.append(key)
            station_info = {
                'Station_Latitude': value[0],
                'Station_Longitude': value[1]
            }
            line_geo.append(station_info)
        line_station_dict = dict(zip(line_station, line_geo))
        line_info[line_name]['Stations'] = line_station_dict

    # retrieve count info from another index
    line_count_res = client.search(index='train_service_passenger_counts_2022_2023', body=query_line_service_count)
    count_info = line_count_res['aggregations']['line']["buckets"]
    for bucket in count_info:
        line_info[bucket["key"]]["Count"] = bucket["doc_count"]

    return json.dumps(line_info)

