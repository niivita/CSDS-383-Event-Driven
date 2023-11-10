#!/usr/bin/env python
import pika
import sys
import requests

# to continually listen for events
# establish a connection:
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='exchange', exchange_type='topic')

# on connect, create a empty queue with an auto-generated name (queue param)
# exclusive= True --> once consu
result = channel.queue_declare('', exclusive=False)
queue_name = result.method.queue

channel.queue_bind(exchange='exchange', queue=queue_name, routing_key="events")
channel.queue_bind(exchange='exchange', queue=queue_name, routing_key="participants")

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}") 
    # FOR ANA AND CALLIE
    # use routing key to see if is "events", then send to the events database, else send to participants


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
