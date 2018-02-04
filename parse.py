import  xml.etree.cElementTree as ET
import os
import gzip
import tarfile

import logging

logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR,filename="./test.log",filemode="a")
#logging.error("testloging")
#read needed counter in conf file
conf = open("pm.conf","rb")
list = [line.strip() for line in conf]
conf.close()
#print list

# unzip .gz file
def un_gz(filename):
    f_name = filename.replace(".gz","")
    g_file = gzip.GzipFile(filename)
    open(f_name,"w+").write(g_file.read())
    g_file.close()

def un_tar_gz(filename):
    tar = tarfile.open(filename)
    names = tar.getnames()
    if os.path.isdir(filename + "_files"):
        pass
    else:
        os.mkdir(filename + "_files")
    for name in names:
        tar.extract(name,filename + "_files/")
    tar.close()

def pasre_pm(Measurements,list):
    PmName = Measurements.find('PmName')

    list1 = []
    for pmcounter in list:
        for child in PmName:
            if(pmcounter == child.text):
                list1.append(child.attrib)

    record = open("record.csv","a+")
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


# parse pm xml
tree = ET.parse("ENB-PM-V2.8.1-EutranCellTdd-20171130-1515P00.xml")
root = tree.getroot()
header = root.find('FileHeader')
vertor = header.find('VendorName').text
for child in root:
    if(child.name == "Measurements"):
        pasre_pm(child,list)





Measurements = root.find('Measurements')
PmName = Measurements.find('PmName')

list1 = []
for pmcounter in list:
    for child in PmName:
        if(pmcounter == child.text):
           list1.append(child.attrib)

#print list1

record = open("record.csv","w")
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