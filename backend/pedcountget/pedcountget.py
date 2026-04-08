from elasticsearch8 import Elasticsearch
import json


def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()
es_username = config('ES_USERNAME')
es_password = config('ES_PASSWORD')
# Connect to Elasticsearch
client = Elasticsearch(
    'https://elasticsearch-master.elastic.svc.cluster.local:9200',
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=(es_username, es_password)  # Use environment variables
)

query = {
    "_source": ["timestamp","sensor_name", "total_of_directions", "location"],
    "query": {
        "match_all": {}
    }
}


def main():
    try:
        response_station_geo = client.search(
            index="pedcount",
            body=query
        )

        ped_info = []
        ped_geo = response_station_geo["hits"]["hits"]

        for geo in ped_geo:
            total_of_directions = geo['_source']['total_of_directions']
            location = geo['_source']['location']
            timestamp = geo['_source']['timestamp']
            sensor_name = geo['_source']['sensor_name']
            longitude = location['lon']
            latitude = location['lat']

            ped_info.append({
                'sensor_name': sensor_name,
                'timestamp': timestamp,
                'Lon': longitude,
                'Lat': latitude,
                'Total of Directions': total_of_directions
            })

        result = json.dumps(ped_info, indent=2)
        print(result)
        return result
    except Exception as e:
        error_msg = json.dumps({"error": str(e)}, indent=2)
        print(error_msg)
        return error_msg

        return json.dumps(ped_info, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

