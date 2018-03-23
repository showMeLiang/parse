import time, sys, pika
from multiprocessing.managers import BaseManager
import  xml.etree.cElementTree as ET
import os
import gzip
import tarfile
import multiprocessing
import logging
import json

def pasre_pm(Measurements):
    PmName = Measurements.find('PmName')
    list1 = []
    for pmcounter in list:
        for child in PmName:
            if(pmcounter == child.text):
                list1.append(child.attrib)
    recordfile = str(os.getpid())+"record.csv"
    print recordfile
    record = open(recordfile,"a+")
    PmData = Measurements.find('PmData')
    for Pm in PmData:
        count = 0
        cell_name = Pm.get('Dn')
        record.write(str(cell_name)+",")
        for key in list1:
            value = ''
            for child in Pm:
                if(child.attrib == key):
                    value = child.text
                    break;
            count += 1
            if (count != len(list1)):
                try:
                    record.write(str(value)+",")
                except e:
                    logging.error(str(e))
            else:
                record.write(str(value))
        record.write('\n')
    record.close()

def parseXML(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    header = root.find('FileHeader')
    vertor = header.find('VendorName').text
    for Measurements in root.findall('Measurements'):
        pasre_pm(Measurements)

def rabbitmq_callback(ch,method,properties, body):
    pool = multiprocessing.Pool(processes = 4)
    files = json.loads(body)
    for file in files:
        pool.apply_async(parseXML,(file,))
        print('running %s' %(file))
    pool.close()
    pool.join()



credentials = pika.PlainCredentials('admin','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost',5672,'/',credentials))
channel = connection.channel()

logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR,filename="./test.log",filemode="a")
conf = open("pm.conf","rb")
list = [line.strip() for line in conf]
conf.close()
pool = multiprocessing.Pool(processes = 4)
channel.basic_consume(rabbitmq_callback,
                      queue='balance',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()