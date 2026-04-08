from elasticsearch8 import Elasticsearch
import json
import logging
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.DEBUG)

url = 'https://127.0.0.1:9200'

username = 'elastic'
password = 'elastic'

client = Elasticsearch(
    [url],
    http_auth=(username, password),
    verify_certs=False
)

query = {
    "_source": ["timestamp", "sensor_name","total_of_directions", "location"],
    "size": 10,
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
                'Longitude': longitude,
                'Latitude': latitude,
                'Total of Directions': total_of_directions
            })

        result = json.dumps(ped_info, indent=2)
        print(result)
        return result
    except Exception as e:
        error_msg = json.dumps({"error": str(e)}, indent=2)
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    main()
