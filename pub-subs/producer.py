#!/usr/bin/env python
import json
import pika

# (install with brew) (add to path)
# sudo rabbitmq-server


# method to be called with some dictionary of information
def publish_event(event_body):
    # establish a connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    channel.exchange_declare(exchange='exchange', exchange_type='topic')

    message = json.dumps(event_body)

    # exchange: tldr- a mediator before queue
    # routing_key: the topic
    channel.basic_publish(exchange='exchange', routing_key='events', body=message)
    print(f" [x] Sent {message}")
    connection.close()


# store a fake event (placeholder for input
fake_event = {"UUID": "1234567",
              "time": "12:11 AM",
              "date": "01/01/2001",
              "title": "birthday",
              "description": "describing",
              "email": "fake_email@gmail.com"}

publish_event(fake_event)
