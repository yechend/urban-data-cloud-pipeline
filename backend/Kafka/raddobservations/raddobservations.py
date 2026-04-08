import json
from flask import current_app, request
from elasticsearch8 import Elasticsearch


def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def main():
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
    current_app.logger.info(f'Observations to add:  {request.get_json(force=True)}')
    request_data = request.get_json(force=True)
    request_json = {"request_data": request_data}


    res = client.index(
        index='robservations',
        body=request_json
    )
    current_app.logger.info(f'Indexed observation successfully')

    return 'ok'
