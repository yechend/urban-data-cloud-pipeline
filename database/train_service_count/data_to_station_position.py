from elasticsearch import Elasticsearch

#  the default elasticsearch configuration
ELASTICSEARCH_HOST_PORT = 'https://localhost:9200'
USER = 'elastic'
ELASTIC_PASSWORD = 'elastic'

es = Elasticsearch(
    ELASTICSEARCH_HOST_PORT,
    basic_auth=(USER, ELASTIC_PASSWORD),
    ssl_show_warn=False,
    verify_certs=False)

query_1 = {
    "size": 0,
    "aggs": {
        "station_name": {
            "terms": {"field": "Station_Name", "size": 500}
        }
    }
}

res_1 = es.search(index='train_service_passenger_counts_2022_2023', body=query_1)
info = res_1['aggregations']['station_name']['buckets']
for bucket in info:
    station = bucket["key"]
    query_2 = {
        "query": {
            "term": {
                "Station_Name": f"{station}"
            }
        },
        "size": 1
    }
    res_2 = es.search(index='train_service_passenger_counts_2022_2023', body=query_2)
    station_info = {
        'Station_Name': station,
        'Station_Latitude': res_2["hits"]["hits"][0]["_source"]['Station_Latitude'],
        'Station_Longitude': res_2["hits"]["hits"][0]["_source"]['Station_Longitude']
    }
    response = es.index(index='station_position', body=station_info)

