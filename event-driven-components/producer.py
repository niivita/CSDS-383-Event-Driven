#!/usr/bin/env python
import json
import pika
from randomgen import *

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def generate_events_and_participants():

    # loop to generate events TODO: increase to 50-100 for final 
    for i in range(1):
        # generate the create event
        event = random_event()
        # publish event
        publish_event(event)

        # loop to generate participants TODO: increase to 5 for final
        for x in range(1): 
            # publish generated participant with same eventID
            publish_participant(random_participant(event["eventID"]))


# method to be called with some dictionary of event information
def publish_event(event_body):
    # parse the input dict 
    message = json.dumps(event_body)

    channel.basic_publish(
        exchange='',
        routing_key='events_queue',
        body= message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    print(f" [x] Sent {message}")

# method to be called with some dictionary of participant information
def publish_participant(event_body):
    # parse the input dict
    message = json.dumps(event_body)
    channel.queue_declare(queue='participants_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='participants_queue',
        body= message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    print(f" [x] Sent {message}")
   

def close_connection():
    connection.close()

generate_events_and_participants()

close_connection()