import json
from elasticsearch8 import Elasticsearch

# Function to read configuration parameters from shared-data
def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
        return f.read()

# Connect to elasticsearch
es_username = config('ES_USERNAME')
es_password = config('ES_PASSWORD')

# connect to Elasticsearch
es_url = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'

client = Elasticsearch(
    es_url,
    basic_auth=(es_username, es_password),
    verify_certs=False,
    ssl_show_warn=False
)

# search data
query = {
    "size": 10000,
    "query": {
        "match_all": {}
    }
}

def main():
    # Execute the Elasticsearch query
    data_dict = dict()
    response = client.search(index="population", body=query)

    # Extract documents from the search response
    data = []
    for hit in response['hits']['hits']:
        source = hit['_source']
        data.append(source)
    # Convert the retrieved data into a dictionary
    for key, values in enumerate(data):
        data_dict[key] = values
    # Return the retrieved data dictionary as a JSON string
    return json.dumps(data_dict)


