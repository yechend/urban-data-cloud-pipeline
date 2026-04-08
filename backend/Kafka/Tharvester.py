import logging, json, requests, socket
from flask import current_app

def main():
    traffic_url = "https://data-exchange-api.vicroads.vic.gov.au/bluetooth_data/links"
    headers_url = {
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": "257b936748224c4b84e8bad2af33ffbb"
    }
    data = requests.get(traffic_url, headers=headers_url).json()
    current_app.logger.info(f'Harvested one traffic observation')

    requests.post(url='http://router.fission/enqueue/traffic',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data)
    )
    return 'OK'
