import json, datetime
from flask import current_app
from kafka import KafkaConsumer, KafkaProducer


def process_message(obs):
    interval_start = obs["properties"].get("lastUpdated")
    if interval_start:
        parsed_timestamp = datetime.datetime.fromisoformat(interval_start)
        formatted_timestamp = parsed_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    else:
        formatted_timestamp = None

    observation = {
            "id": obs["properties"].get("id"),
            "sourceName": obs["properties"].get("source", {}).get("sourceName"),
            "sourceId": obs["properties"].get("source", {}).get("sourceId"),
            "status": obs["properties"].get("status"),
            "closedRoadName": obs["properties"].get("closedRoadName"),
            "eventType": obs["properties"].get("eventType"),
            "eventDueTo": obs["properties"].get("eventDueTo"),
            "ImpactDirection": obs["properties"].get("impact", {}).get("direction"),
            "ImpactType": obs["properties"].get("impact", {}).get("impactType"),
            "numberLanesImpacted": obs["properties"].get("impact", {}).get("numberLanesImpacted"),
            "speedLimitOnSite": obs["properties"].get("impact", {}).get("speedLimitOnSite"),
            "durationstart": obs["properties"].get("duration", {}).get("start"),
            "durationend": obs["properties"].get("duration", {}).get("end"),
            "lastUpdated": formatted_timestamp
    }

    return observation

def main():
    consumer = KafkaConsumer(
        'road',
        bootstrap_servers=['my-cluster-kafka-bootstrap.kafka.svc:9092'],
        group_id='my-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    current_app.logger.info(f'Processed a Road observation')

    producer = KafkaProducer(bootstrap_servers='my-cluster-kafka-bootstrap.kafka.svc:9092')


    for message in consumer:
        kafka_message = message.value
        current_app.logger.info(f'Processed a traffic observation')

        features = kafka_message.get('features', [])

        for obs in features:
            observation = process_message(obs)
            observation_json = json.dumps(observation)
            producer.send('robservations', value=observation_json.encode('utf-8'))

    current_app.logger.info(f'Processed all traffic observations')

    consumer.close()
    producer.close()

    return {
        "status": 200,
        "body": "Processed observations sent to 'observations' topic."
    }

