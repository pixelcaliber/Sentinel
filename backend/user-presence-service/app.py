import logging
import os
from threading import Thread

import firebase_admin
import requests
from confluent_kafka import Consumer, KafkaError
from firebase_admin import credentials, messaging
from flask import Flask, json, request

cred = credentials.Certificate(
    "/Users/abhinavpandey/Desktop/chat-application/notif-service/serviceAccountsKey.json"
)
firebase_admin.initialize_app(cred)

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

fcm_token = os.environ.get("fcm_token")

consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my_consumer_group",
    "auto.offset.reset": "earliest",
}
consumer = Consumer(consumer_config)
consumer.subscribe(["received_messages"])


def kafka_consumer():
    while True:
        msg = consumer.poll(10000)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logging.info(msg.error())
                break

        kafka_message = msg.value().decode("utf-8")

        kafka_message_dict = json.loads(kafka_message)

        logging.info(f"Received Kafka message:{kafka_message_dict}")

        url = "http://localhost:8000/send_notification"

        # Convert the dictionary to JSON
        json_data = json.dumps(kafka_message_dict)

        requests.post(url, json=json_data)


kafka_thread = Thread(target=kafka_consumer)
kafka_thread.start()


@app.route("/", methods=["POST", "GET"])
def health():
    return "Server is running fine and listening to port 8000"


@app.route("/send_notification", methods=["POST", "GET"])
def send_notification():
    data_dict = request.json
    header = data_dict.get("header")
    body = data_dict.get("body")
    message = messaging.Message(
        data={
            "header": header,
            "body": body,
        },
        token=fcm_token,
    )

    response = messaging.send(message)
    print("Successfully sent message:", response)
    return f"Successfully sent message: {response}"


if __name__ == "__main__":
    app.run(port=8000)
