from elasticsearch import Elasticsearch

#  the default elasticsearch configuration
ELASTICSEARCH_HOST_PORT = 'https://localhost:9200'
USER = 'elastic'
ELASTIC_PASSWORD = 'elastic'
INDEX_NAME = 'train_service_passenger_counts_2022_2023'

es = Elasticsearch(
    ELASTICSEARCH_HOST_PORT,
    basic_auth=(USER, ELASTIC_PASSWORD),
    ssl_show_warn=False,
    verify_certs=False)

# 创建索引
# year = ['2018_2019', '2019_2020', '2020_2021', '2021_2022', '2022_2023']
# index_name = f"train_service_passenger_counts_{year[4]}"
# index_name = 'demo'
request_body = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "Business_Date": {"type": "date"},
            "Day_of_Week": {"type": "keyword"},
            "Day_Type": {"type": "keyword"},
            "Mode": {"type": "keyword"},
            "Train_Number": {"type": "keyword"},
            "Line_Name": {"type": "keyword"},
            "Group": {"type": "keyword"},
            "Direction": {"type": "keyword"},
            "Origin_Station": {"type": "keyword"},
            "Destination_Station": {"type": "keyword"},
            "Station_Name": {"type": "keyword"},
            "Station_Latitude": {"type": "float"},
            "Station_Longitude": {"type": "float"},
            "Station_Chainage": {"type": "integer"},
            "Stop_Sequence_Number": {"type": "integer"},
            "Arrival_Time_Scheduled": {"type": "keyword"},
            "Departure_Time_Scheduled": {"type": "keyword"},
            "Passenger_Boardings": {"type": "integer"},
            "Passenger_Alightings": {"type": "integer"},
            "Passenger_Arrival_Load": {"type": "integer"},
            "Passenger_Departure_Load": {"type": "integer"}
        }
    }
}

es.indices.create(index=INDEX_NAME, body=request_body)
