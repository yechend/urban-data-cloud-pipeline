import datetime, requests
from flask import current_app
from elasticsearch8 import Elasticsearch, helpers
from concurrent.futures import ThreadPoolExecutor

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

def fetch_data():
    traffic_url = "https://data-exchange-api.vicroads.vic.gov.au/bluetooth_data/sites"
    headers = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": "257b936748224c4b84e8bad2af33ffbb"
    }
    response = requests.get(traffic_url, headers=headers)
    if response.status_code == 200:
        current_app.logger.info('Data retrieved successfully from API.')
        return response.json()
    else:
        current_app.logger.error(f'Failed to retrieve data: {response.status_code}')
        return []

def process_data(data):
    observations = []
    for obs in data:
        interval_start = obs["latest_stats"].get("interval_start")
        if interval_start:
            parsed_timestamp = datetime.datetime.fromisoformat(interval_start)
            formatted_timestamp = parsed_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            formatted_timestamp = None
        observation = {
            "id": obs.get("id"),
            "number": obs.get("number"),
            "enabled": obs.get("enabled"),
            "name": obs.get("name"),
            "location": obs.get("location"),
            "latest_stats": {
                "interval_start": formatted_timestamp
            }
        }
        observations.append(observation)
    return observations

def bulk_upload(client, actions):
    try:
        helpers.bulk(client, actions)
        current_app.logger.info('Bulk upload successful')
    except Exception as e:
        current_app.logger.error(f'Error during bulk upload: {e}')

def main():
    data = fetch_data()
    if not data:
        return

    observations = process_data(data)
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

    chunk_size = 1000
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(0, len(observations), chunk_size):
            chunk = observations[i:i + chunk_size]
            actions = [{"_index": "sites", "_source": record} for record in chunk]
            executor.submit(bulk_upload, client, actions)

    return 'ok'