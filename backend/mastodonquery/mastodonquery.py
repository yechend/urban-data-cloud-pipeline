"""
File: mastodonquery.py
Author: Yechen Deng
Date: 21/05/2024
Description: This program send an query to ES to harvest data from 2024-05-20 to 2024-05-26 for analysis.
"""
import json
import logging
from datetime import datetime
from elasticsearch8 import Elasticsearch

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Extract config maps
def config(k):
    with open(f'/configs/default/shared-mastodon/{k}', 'r') as f:
        return f.read()

es_username = config('ES_USERNAME')
es_password = config('ES_PASSWORD')

client = Elasticsearch(
    'https://elasticsearch-master.elastic.svc.cluster.local:9200',
    verify_certs=False,
    ssl_show_warn=False,
    basic_auth=(es_username, es_password)  # Use environment variables
)

def create_query(start_date, end_date):
    return {
        "query": {
            "range": {
                "created_at": {
                    "gte": start_date,
                    "lte": end_date,
                    "format": "yyyy-MM-dd"
                }
            }
        },
        "sort": [{"created_at": {"order": "asc"}}],
        "size": 10000
    }

def process_hits(hits):
    hourly_stats = {}
    for hit in hits:
        doc = hit['_source']
        timestamp = doc['created_at']
        # Adjust to use datetime including the hour
        date_format = '%Y-%m-%dT%H:%M:%S.%f' if '.' in timestamp else '%Y-%m-%dT%H:%M:%S'
        date_key = datetime.strptime(timestamp, date_format)
        hour_str = date_key.strftime('%Y-%m-%dT%H')  # Create a string that includes the hour

        if hour_str not in hourly_stats:
            hourly_stats[hour_str] = {
                'average_sentiment': 0,
                'doc_count': 0,
                'cumulative_airquality': 0,
                'cumulative_traffic': 0,
                'cumulative_weather': 0
            }

        stats = hourly_stats[hour_str]
        stats['doc_count'] += 1
        current_total_sentiment = stats['average_sentiment'] * (stats['doc_count'] - 1)
        current_total_sentiment += doc['sentiment']
        stats['average_sentiment'] = current_total_sentiment / stats['doc_count']
        stats['cumulative_airquality'] += doc['count_airquality']
        stats['cumulative_traffic'] += doc['count_traffic']
        stats['cumulative_weather'] += doc['count_weather']

    return hourly_stats

def main():
    start_date = "2024-05-20"
    end_date = "2024-05-26"
    query = create_query(start_date, end_date)
    try:
        response = client.search(index="mastodonau", body=query)
        hourly_stats = process_hits(response['hits']['hits'])
        return json.dumps(hourly_stats, indent=4)
    except Exception as e:
        logging.error(f"An error occurred: {e}")