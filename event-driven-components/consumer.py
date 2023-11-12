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


    # TODO: FOR ANA AND CALLIE
    # method.routing_key.split('_')[0] will be either "events" or "participants":
    # use routing key to see if is "events", then send to the events database, else send to participants
    url= "https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/participants/?"
    if method.routing_key.split(' ')[0] == "participants_queue":
        print("Inserting participant:")
        data = json.loads(body.decode('UTF-8'))
        print(dict(data))
        x = requests.post(url+urllib.parse.urlencode(data))
        print(x)
    else:
        print("Not inserting anything")
        print(method.routing_key.split(' '))

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='events_queue', on_message_callback=callback)
channel.basic_consume(queue='participants_queue', on_message_callback=callback)

channel.start_consuming()
