#!/usr/bin/env python
import pika
import time
import requests
import json
import urllib.parse

# to continually listen for events
# establish a connection:
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='events_queue', durable=True)
channel.queue_declare(queue='participants_queue', durable=True)

print(' [*] Waiting to receive requests. To exit press CTRL+C')

# result = channel.queue_declare('', exclusive=False)
# queue_name = result.method.queue

# channel.queue_bind(exchange='exchange', queue=queue_name, routing_key="events")
# channel.queue_bind(exchange='exchange', queue=queue_name, routing_key="participants")


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}") 
    time.sleep(body.count(b'.'))
    ch.basic_ack(delivery_tag=method.delivery_tag)

    #Insertion calling API
    participant_url= "https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/participants/?"
    event_url= "https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/events/?"
    #participants
    if method.routing_key.split(' ')[0] == "participants_queue":
        print("Inserting participant:")
        params = json.loads(body.decode('UTF-8'))
        #posting using url params
        response = requests.post(participant_url+urllib.parse.urlencode(params))
        print(str(response) + ": Participant added successfully")
    #events
    elif method.routing_key.split(' ')[0] == "events_queue":
        print("Inserting event:")
        params = json.loads(body.decode('UTF-8'))
        #posting using url params
        response = requests.post(event_url+urllib.parse.urlencode(params))
        print(str(response) + ": Event added successfully")
    else:
        print("Not inserting anything")
        print(method.routing_key.split(' '))

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='events_queue', on_message_callback=callback)
channel.basic_consume(queue='participants_queue', on_message_callback=callback)

channel.start_consuming()
