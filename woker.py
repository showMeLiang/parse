import time, sys, Queue
from multiprocessing.managers import BaseManager
import  xml.etree.cElementTree as ET
import os
import gzip
import tarfile
import multiprocessing
import logging
# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

def pasre_pm(Measurements):
    PmName = Measurements.find('PmName')
    list1 = []
    for pmcounter in list:
        for child in PmName:
            if(pmcounter == child.text):
                list1.append(child.attrib)
    recordfile = os.getpid()+"record.csv"
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


# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行taskmanager.py的机器:
server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与taskmanager.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey='abc')
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR,filename="./test.log",filemode="a")
conf = open("pm.conf","rb")
list = [line.strip() for line in conf]
conf.close()
pool = multiprocessing.Pool(processes = 4)
# 从task队列取任务,并把结果写入result队列:
while Queue.qsize>0:
    try:
        n = task.get(timeout=1)
        print('run task %s...' % (n))
        pool.apply_async(parseXML,(n,))
        r = "finish" 
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task queue is empty.')
# 处理结束:
pool.close()
pool.join()
print('worker exit.')