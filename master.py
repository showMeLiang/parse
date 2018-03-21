import pika
from multiprocessing.managers import BaseManager

credentials = pika.PlainCredentials('admin','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.163.129',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='balance')
list = ["test.xml","test1.xml","test2.xml","test3.xml"]

for file in list:
    channel.basic_publish(exchange='',
                      routing_key='balance',
                      body=file)
    print ("Sent %s",%(file))
connection.close()
