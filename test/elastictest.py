import logging
import json
import os
from flask import Flask, current_app
from elasticsearch8 import Elasticsearch


def main():
    json_file_path = "C:\\Users\\22759\\Desktop\\pedcont.json"

    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        es_url = 'https://127.0.0.1:9200'
        es_username = 'elastic'
        es_password = 'elastic'

        client = Elasticsearch(
            es_url,
            basic_auth=(es_username, es_password),
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=1200
        )

        current_app.logger.info('Data to add to Elasticsearch')


        res = client.index(
            index='pedcount',
            body=data
        )
        current_app.logger.info(f'Indexed data successfully: {res["_id"]}')
    except Exception as e:
        current_app.logger.error(f'An error occurred: {str(e)}')

    return 'ok'


if __name__ == "__main__":
    app = Flask(__name__)
    with app.app_context():
        main()
