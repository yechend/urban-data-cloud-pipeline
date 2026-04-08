import json, datetime
from flask import current_app
from kafka import KafkaConsumer


def main():
    consumer = KafkaConsumer(
        'traffic',
        bootstrap_servers=['my-cluster-kafka-bootstrap.kafka.svc:9092'],
        group_id='my-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    current_app.logger.info(f'Processed a traffic observation')
    #kafka_message = context.request.get_data().decode('utf-8')

    observations = []

    for message in consumer:
        kafka_message = message.value
        current_app.logger.info(f'Processed a traffic observation: {kafka_message}')

        for obs in kafka_message:
            interval_start = obs["latest_stats"].get("interval_start")
            if interval_start:
                parsed_timestamp = datetime.datetime.fromisoformat(interval_start)
                formatted_timestamp = parsed_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            else:
                formatted_timestamp = None
            observation = {
                "id": obs.get("id"),
                "name": obs.get("name"),
                "organization": {
                    "id": obs["organization"].get("id")
                },
                "origin": {
                    "id": obs["origin"].get("id")
                },
                "destination": {
                    "id": obs["destination"].get("id")
                },
                "latest_stats": {
                    "interval_start": formatted_timestamp,
                    "travel_time": obs["latest_stats"].get("travel_time"),
                    "delay": obs["latest_stats"].get("delay"),
                    "speed": obs["latest_stats"].get("speed"),
                    "excess_delay": obs["latest_stats"].get("excess_delay"),
                    "congestion": obs["latest_stats"].get("congestion"),
                    "score": obs["latest_stats"].get("score"),
                    "flow_restriction_score": obs["latest_stats"].get("flow_restriction_score"),
                    "average_density": obs["latest_stats"].get("average_density"),
                    "density": obs["latest_stats"].get("density"),
                    "enough_data": obs["latest_stats"].get("enough_data"),
                    "ignored": obs["latest_stats"].get("ignored"),
                    "closed": obs["latest_stats"].get("closed"),
                    "estimated_percent": obs["latest_stats"].get("estimated_percent")
                }
            }
            observations.append(observation)

    return {
        "status": 200,
        "body": json.dumps(observations)
    }
