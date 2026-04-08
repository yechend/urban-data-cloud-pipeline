"""
File: mharvester.py
Author: Yechen Deng
Date: 20/05/2024
Description: This program harvests toots from mastodon.au after its first running - the first harvested toot time
"""
import sys
import json
import re
import requests
import logging
import nltk
import lxml
from datetime import datetime, timedelta
from time import sleep
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import TextBlob
from bs4 import BeautifulSoup
from elasticsearch8 import Elasticsearch, helpers
from flask import Flask, current_app

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Target servers
SERVER1 = "mastodon.au"
SERVER2 = "aus.social"

# Preprocessed keywords from three topics
token_weather = [
    'forecast', 'fog', 'chill', 'sunris', 'cyclon', 'muggi', 'blusteri', 'dew', 'cold', 'humid', 'snowfal', 'temper',
    'snow', 'westerli', 'surg', 'atmospher', 'downpour', 'avalanch', 'rainbow', 'moistur', 'gale', 'weather', 'pressur',
    'frost', 'climat', 'summer', 'sleet', 'balmi', 'easterli', 'flood', 'whirlwind', 'winter', 'sunset', 'gust', 'icicl',
    'wave', 'permafrost', 'thunder', 'lightn', 'humid', 'air', 'front', 'shower', 'warm', 'breez', 'heat', 'storm',
    'thunderstorm', 'temperatur', 'monsoon', 'water', 'drizzl', 'dri', 'autumn', 'tornado', 'cycl', 'index', 'mist',
    'overcast', 'isobar', 'drought', 'sky', 'barometr', 'cloudi', 'cloud', 'smog', 'hurrican', 'gaug', 'hail','ozon',
    'flash', 'blizzard', 'freez', 'tropic', 'wind', 'condens', 'ice', 'spring', 'snap', 'rain']
token_traffic = [
    'airplan', 'merchandis', 'citi', 'car', 'side', 'vehicl', 'thoroughfar', 'eas', 'deal', 'intersect', 'speed',
    'park', 'railway', 'crosswalk', 'interchang', 'taxiway', 'navig', 'speeder', 'toll', 'bu', 'expressway',
    'transmiss', 'underpass', 'offramp', 'signal', 'plaza', 'weather', 'street', 'safeti', 'commerc', 'stop', 'road',
    'back', 'stoplight', 'transit', 'highway', 'crowd', 'congest', 'peopl', 'jam', 'westbound', 'aviat', 'accid',
    'commut', 'gridlock', 'light', 'speed', 'view', 'transport', 'signag', 'busiest', 'transport', 'polic', 'sign',
    'accid', 'roadwork', 'block', 'cross', 'southbound', 'rerout', 'drive', 'traffic', 'motorist', 'roadwork', 'vehicl',
    'jam', 'truck', 'lane', 'highway', 'northbound', 'mercantil', 'public', 'passeng', 'road', 'limit', 'ramp', 'cargo',
    'time', 'snarl', 'interst', 'roadway', 'freeway', 'pedestrian', 'mark', 'pedestrian', 'airport', 'volum', 'commerci',
    'block', 'exit', 'car', 'travel']
token_air_quality = [
    'dust', 'blimp', 'pet', 'carcinogen', 'airstrip', 'carpet', 'reair', 'airdrop', 'aerostat', 'airspac', 'pesticid',
    'unbreath', 'chronic', 'airbu', 'asthma', 'airtight', 'qualityairless', 'breathabl', 'airward', 'atmospher',
    'anthropogen', 'pneumonia', 'atmospher', 'pneumocephalu', 'tetrachloroethylen', 'airwav', 'plywood', 'turbul',
    'aeromet', 'pneumoperitoneum', 'garden', 'ventil', 'airward', 'nitrogen', 'mold', 'airi', 'aura', 'aerial', 'xenon',
    'sulfur', 'obstruct', 'carbon', 'airsick', 'airomet', 'inflamm', 'krypton', 'pyopneumothorax', 'fresh', 'environ',
    'plumb', 'pneumat', 'argon', 'lung', 'incens', 'stroke', 'airfram', 'physometra', 'ga', 'earth', 'ventil', 'dioxid',
    'tonn', 'built', 'particul', 'natur', 'airscrew', 'aero', 'smog', 'airlinerbiomolecul', 'asbesto', 'ozon', 'aerifi',
    'monoxid', 'pneumat', 'charcoal', 'airborn', 'aerifer', 'deaerat', 'aerat', 'asbestosi', 'fireplac', 'dyspnea',
    'pollen', 'formaldehyd']

# Preprocess contents from harvested toots
def get_tokens(content):
    # Helper functions
    def remove_unicode(text):
        # Normalize to ASCII
        return text.encode('ascii', 'ignore').decode()

    def clean_text(text):
        # Convert to lowercase
        text = text.lower()
        # Remove URLs, handles, numbers, and any non-alphabetic characters
        text = re.sub(r"http\S+|www\S+|@\S+|#\S+|\d+", '', text)
        # Replace unwanted characters with spaces
        text = re.sub(r"[^a-z\s]", ' ', text)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    # Tokenization, stop word removal, and stemming
    def tokenize_and_process(text):
        stop_words = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        tokens = nltk.word_tokenize(text)
        processed_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words and len(word) > 2]
        return processed_tokens

    # Apply functions
    content = remove_unicode(content)
    content = clean_text(content)
    tokens = tokenize_and_process(content)
    return tokens

# Remove html tags
def remove_html_tags(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    return ''.join(soup.find_all(string=True))

# Process html and extract mention infos
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    paragraph = soup.find('p')
    if paragraph is None:
        return None
    mention = paragraph.find('a', attrs={'class': 'mention hashtag'})
    return mention

# Main functionality to extract toots details
def extract_post_info(post_data, previous_cumulative_counts=None):
    created_at = datetime.strptime(post_data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    post_info = {
        'id': post_data['id'],
        'created_at': created_at.isoformat(),
        'lang': post_data['language'],
        'tags': [tag['name'] for tag in post_data['tags']]
    }

    raw_html = post_data['content']
    # Extract sentiment (using TextBlob)
    text = remove_html_tags(post_data['content'])
    post_info['sentiment'] = TextBlob(text).sentiment.polarity
    # Extract tokens (after cleaning HTML tags and preprocessing text)
    tokens = get_tokens(text)
    post_info['tokens'] = tokens

    # Extract tags
    mentions_or_hashtags = parse_html(raw_html)
    if mentions_or_hashtags:
        post_info['mentions_or_hashtags'] = mentions_or_hashtags.get_text()

    # Count occurrences of weather, traffic, and air quality in tokens
    count_weather = sum(1 for token in tokens if token in token_weather)
    count_traffic = sum(1 for token in tokens if token in token_traffic)
    count_airquality = sum(1 for token in tokens if token in token_air_quality)

    # Calculate cumulative sums
    if previous_cumulative_counts:
        cumul_sum_weather = previous_cumulative_counts['cumul_sum_weather'] + count_weather
        cumul_sum_traffic = previous_cumulative_counts['cumul_sum_traffic'] + count_traffic
        cumul_sum_airquality = previous_cumulative_counts['cumul_sum_airquality'] + count_airquality
    else:
        cumul_sum_weather = count_weather
        cumul_sum_traffic = count_traffic
        cumul_sum_airquality = count_airquality

    # Add counts and cumulative sums to post_info
    post_info['count_weather'] = count_weather
    post_info['count_traffic'] = count_traffic
    post_info['count_airquality'] = count_airquality
    post_info['cumul_sum_weather'] = cumul_sum_weather
    post_info['cumul_sum_traffic'] = cumul_sum_traffic
    post_info['cumul_sum_airquality'] = cumul_sum_airquality

    return post_info

# Read the starting state
def read_state(prefix,es):
    es = es
    """Reads the complete state from Elasticsearch index."""
    index_name = "mastodonausstate"
    default_state = {
        'last_id': None,
        'record_count': 0,
        'cumul_sum_weather': 0,
        'cumul_sum_traffic': 0,
        'cumul_sum_airquality': 0
    }
    try:
        # Query to get the latest document based on a specific logic
        query = {
            "size": 1
        }
        response = es.search(index=index_name, body=query)
        print(response)
        if response['timed_out'] == True:
            response = es.search(index=index_name, body=query)
        if response['hits']['hits']:
            state = response['hits']['hits'][0]['_source']
            # Ensure all keys are present, else use default
            for key in default_state:
                if key not in state:
                    state[key] = default_state[key]
            return state['record_count'], state['last_id'], state
        else:
            return default_state['record_count'], default_state['last_id'], default_state
    except Exception as e:
        print(f"Failed to read from Elasticsearch: {e}")
        return default_state['record_count'], default_state['last_id'], default_state

# Update the state to the defined index
def update_state(prefix, max_id, record_count, cumulative_counts_1,es):
    es = es
    # Create or update a document that represents the current state
    document_id = f"{prefix}_state"  # Unique ID for the state document
    if "cumulative_counts" not in cumulative_counts_1.keys():
        state_document = {
            'last_id': max_id,
            'record_count': record_count,
            'cumulative_counts': {
                'weather': cumulative_counts_1['cumul_sum_weather'],
                'traffic': cumulative_counts_1['cumul_sum_traffic'],
                'airquality': cumulative_counts_1['cumul_sum_airquality']
            }
        }
    else:
        state_document = {
            'last_id': max_id,
            'record_count': record_count,
            'cumulative_counts': {
                'weather': cumulative_counts_1['cumulative_counts']['weather']
                           + cumulative_counts_1['cumul_sum_weather'],
                'traffic': cumulative_counts_1['cumulative_counts']['traffic']
                           + cumulative_counts_1['cumul_sum_traffic'],
                'airquality': cumulative_counts_1['cumulative_counts']['airquality']
                              + cumulative_counts_1['cumul_sum_airquality']
        }
    }

    try:
        response = es.index(index="mastodonausstate", id=document_id, document=state_document)
        print(f"State updated in Elasticsearch for {document_id}: {response}")
    except Exception as e:
        print(f"Error updating state in Elasticsearch for {document_id}: {str(e)}")

# Creating timelines
def create_timelines_url(instance_url: str, max_id: str = None, local: bool = False):
    params = "limit=40" + (f"&max_id={max_id}" if max_id else '') + ("&local=true" if local else '')
    return f"{instance_url}/api/v1/timelines/public?{params}"

# Determine the timelines of each toot and starting state for the program
def get_timelines(access_token, instance_url, nyears, es):
    es = es
    index_name = "mastodonau"
    headers = {'Authorization': f'Bearer {access_token}'}
    server_name = instance_url.split('//')[-1].split('.')[0]
    state_file_prefix = f"{server_name}_state"
    default_state = {
        'last_id': None,
        'record_count': 0,
        'cumul_sum_weather': 0,
        'cumul_sum_traffic': 0,
        'cumul_sum_airquality': 0
    }
    last_fetched_record, max_id, cumulative_counts = read_state(state_file_prefix, es)
    date_limit = datetime.now() - timedelta(days=365 * nyears)
    count = last_fetched_record
    bulk_data = []

    while True:
        search_url = create_timelines_url(instance_url, max_id)
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if not data:
                current_app.logger.info("No more data returned.")
                break
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error during requests to API: {e}")
            break

        for status in data:
            created_at = datetime.strptime(status['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            current_app.logger.debug(f"Processing status from {status['created_at']}")
            if created_at < date_limit:
                current_app.logger.info("Reached the date limit for fetching statuses.")
                break

            post_info = extract_post_info(status, cumulative_counts)
            if post_info:
                cumulative_counts['cumul_sum_weather'] = post_info['cumul_sum_weather']
                cumulative_counts['cumul_sum_traffic'] = post_info['cumul_sum_traffic']
                cumulative_counts['cumul_sum_airquality'] = post_info['cumul_sum_airquality']
                count += 1
                bulk_data.append({"_index": index_name, "_source": post_info})

            max_id = status['id']
            print(cumulative_counts)
            # Introduce a delay of 1 second between each request
            sleep(1)

        if bulk_data:
            current_app.logger.info("Sending bulk data to Elasticsearch.")
            helpers.bulk(es, bulk_data)
            bulk_data = []

        if count >= 40:
            current_app.logger.info("Reached the limit of 40 posts.")
            break

        if 'error' in data and data["error"] == "Too many requests":
            current_app.logger.warning("Too many requests. Sleeping for 10 seconds.")
            sleep(10)
            continue

    update_state(state_file_prefix, max_id, count, cumulative_counts,es)  # Final state update
    current_app.logger.info(f"Updated state with max_id: {max_id}, last_fetched_record: {count}")
    return count

# Extract config maps
def config(k):
    with open(f'/configs/default/shared-mastodon/{k}', 'r') as f:
        return f.read()

es_username = config('ES_USERNAME')
es_password = config('ES_PASSWORD')
token1 = config('MASTODON_AU_TOKEN')
token2 = config('MASTODON_SOCIAL_TOKEN')

# The main function to run this harvesting program
def main():
    es_url = 'https://elasticsearch-master.elastic.svc.cluster.local:9200'

    # Connect to Elasticsearch
    es = Elasticsearch(
        es_url,
        basic_auth=(es_username, es_password),
        verify_certs=False,
        ssl_show_warn=False
    )
    current_app.logger.info("Connected to Elasticsearch.")
    N_YEARS = 1  # Represents 1 year
    index_name = f"{SERVER1.replace('.', '')}"
    if token1 is None:
        current_app.logger.error(f"Error: No token found for server {SERVER1}")

    try:
        current_app.logger.info(f"Start fetching {SERVER1}")
        count = get_timelines(token1, f"https://{SERVER1}", N_YEARS, es)
        current_app.logger.info(f"Fetched {count} posts from {SERVER1}")
    except Exception as e:
        current_app.logger.error(f"Error processing {SERVER1}: {str(e)}")
    return 'Succeed Harvesting'