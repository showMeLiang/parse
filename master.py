import pika
import json
from multiprocessing.managers import BaseManager

credentials = pika.PlainCredentials('admin','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='balance')
list = ["test_pm.xml","test_pm1.xml","test_pm2.xml","test_pm3.xml"]
jdata = json.dumps(list)
for file in list:
    channel.basic_publish(exchange='',
                      routing_key='balance',
                      body=jdata)
    print jdata
connection.close()
