#!/usr/bin/env python
import json
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# TODO: generation 
def generate_events_and_participants():

    # store a fake event (placeholder for generated input)
    fake_event = {"eventID": "1234567",
              "time": "12:11 AM",
              "date": "01/01/2001",
              "title": "birthday",
              "description": "describing",
              "email": "fake_email@gmail.com"}
    publish_event(fake_event)

    # store a fake participant (placeholder for generated input)
    fake_participant = {"participantID": "987654", 
                        "eventID": "1234567", 
                        "name": "Bob",
                        "email": "email@yahoo.com"}

    publish_participant(fake_participant)


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