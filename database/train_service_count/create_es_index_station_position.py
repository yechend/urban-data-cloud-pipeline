from elasticsearch import Elasticsearch

#  the default elasticsearch configuration
ELASTICSEARCH_HOST_PORT = 'https://localhost:9200'
USER = 'elastic'
ELASTIC_PASSWORD = 'elastic'
INDEX_NAME = 'station_position'

es = Elasticsearch(
    ELASTICSEARCH_HOST_PORT,
    basic_auth=(USER, ELASTIC_PASSWORD),
    ssl_show_warn=False,
    verify_certs=False)

request_body = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "Station_Name": {"type": "keyword"},
            "Station_Latitude": {"type": "float"},
            "Station_Longitude": {"type": "float"}
        }
    }
}

es.indices.create(index=INDEX_NAME, body=request_body)

