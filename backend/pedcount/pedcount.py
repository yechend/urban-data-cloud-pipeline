import json, requests
import logging
from flask import Flask, current_app
from elasticsearch8 import Elasticsearch, helpers

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def read_json_in_chunks(data, chunk_size=10000):
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]

def main():
    data_url = 'https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/pedestrian-counting-system-monthly-counts-per-hour/exports/json?limit=-1&timezone=UTC&use_labels=false&epsg=4326'
    response = requests.get(data_url)
    data = response.json()
    try:
        es_url = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'
        es_username = config('ES_USERNAME')
        es_password = config('ES_PASSWORD')

        client = Elasticsearch(
            es_url,
            basic_auth=(es_username, es_password),
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=1200
        )

        current_app.logger.info('Data to add to Elasticsearch')

        for chunk in read_json_in_chunks(data):
            actions = [
                {
                    "_index": "pedcount",
                    "_source": record
                }
                for record in chunk
            ]
            helpers.bulk(client, actions)
            current_app.logger.info(f'Indexed chunk of data successfully')
    except Exception as e:
        current_app.logger.error(f'An error occurred: {str(e)}')

    return 'ok'


# if __name__ == "__main__":
#     app = Flask(__name__)
#     with app.app_context():
#         main()
