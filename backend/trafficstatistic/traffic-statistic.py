import logging
import json
from flask import request, jsonify
from elasticsearch8 import Elasticsearch
from string import Template

# Elasticsearch server URL
def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

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
# query traffic data
query_template = Template('''{
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "id": "${id}"
                    }
                },
                {
                    "range": {
                        "latest_stats.interval_start": {
                            "gte": "${date} 00:00:00",
                            "lt": "${date} 23:59:59"
                        }
                    }
                }
            ]
        }
    },
    "aggs": {
        "congestion_per_hour": {
            "date_histogram": {
                "field": "latest_stats.interval_start",
                "calendar_interval": "hour"
            },
            "aggs": {
                "average_congestion": {
                    "avg": {
                        "field": "latest_stats.congestion"
                    }
                }
            }
        }
    },
    "size": 0
}''')


def main():
    try:
        date = request.headers['X-Fission-Params-Date']
    except KeyError:
        date = None
    try:
        id = request.headers['X-Fission-Params-id']
    except KeyError:
        id = None

    query = query_template.substitute(date=date, id=id)

    # 打印生成的查询字符串
    logging.info(f"Generated query: {query}")
    try:
        query_dict = json.loads(query)
    except json.JSONDecodeError as e:
        logging.error(f"JSONDecodeError: {e}")
        return jsonify({"error": "Invalid JSON format in query"}), 500

    # index traffic data
    logging.info("indexing then traffic statistics...")
    response_traffic_data = client.search(index="traffic", body=query_dict)

    # get the congestion
    congestion_info = []
    buckets = response_traffic_data['aggregations']['congestion_per_hour']['buckets']
    for bucket in buckets:
        key_as_string = bucket['key_as_string']
        average_congestion = bucket['average_congestion']['value']
        congestion_info.append({
            'Time': key_as_string,
            'average_congestion_per_hour': average_congestion
        })

    #return congestion_info
    return json.dumps(congestion_info, indent=2)
