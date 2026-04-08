import logging
import json
import os
from elasticsearch8 import Elasticsearch


def main():
    # local json file downloaded from SUDO
    json_file_path = "C:/Users/jocel/Desktop/master/comp90024/a2/abs_regional_population_summary_sa2_2019-5528703085463955838.json"

    try:
        # read json file
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        cleaned_data=[]
        # process the data in correct format and only keep the necessary data
        for feature in data['features']:
            population = {
                "persons_num": feature["properties"]["persons_num"],
                "percentage_person_aged_0_14": feature["properties"]["percentage_person_aged_0_14"],
                "percentage_person_aged_15_64": feature["properties"]["percentage_person_aged_15_64"],
                "percentage_person_aged_65_plus": feature["properties"]["percentage_person_aged_65_plus"],
                "feature_name": feature["properties"]["feature_name"],
            }
            cleaned_data.append(population)
        # Connect to Elasticsearch
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

        logging.info('Data to add to Elasticsearch')
        # upload the file to elasticsearch one by one
        for item in cleaned_data:
            res = client.index(
                index='population',
                body=item
            )
        logging.info(f'Indexed data successfully: {res["_id"]}')
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')

    return 'ok'


if __name__ == "__main__":
        main()
