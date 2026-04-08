from elasticsearch import Elasticsearch

#  the default elasticsearch configuration
ELASTICSEARCH_HOST_PORT = 'https://localhost:9200'
USER = 'elastic'
ELASTIC_PASSWORD = 'elastic'
INDEX_NAME = 'transport_line_information'

es = Elasticsearch(
    ELASTICSEARCH_HOST_PORT,
    basic_auth=(USER, ELASTIC_PASSWORD),
    ssl_show_warn=False,
    verify_certs=False)

request_body = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "Line_Name": {"type": "keyword"},
            "Line_Mode": {"type": "keyword"},
            "Group": {"type": "keyword"},
            "Stations_Number": {"type": "integer"},
            "Stations": {
                "type": "nested",
                "properties": {
                    "name": {
                        "type": "keyword"
                    },
                    "geo_info": {
                        "type": "text"
                    }
                }
            }
        }
    }
}

es.indices.create(index=INDEX_NAME, body=request_body)
