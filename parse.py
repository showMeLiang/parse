import  xml.etree.cElementTree as ET
import os
import gzip
import tarfile

#read needed counter in conf file
conf = open("pm.conf","rb")
list = [line.strip() for line in conf]
conf.close()
print list

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

# parse pm xml
tree = ET.parse("test_pm.xml")
root = tree.getroot()
header = root.find('FileHeader')
vertor = header.find('VendorName').text
Measurements = root.find('Measurements')
PmName = Measurements.find('PmName')

list1 = []
for pmcounter in list:
    for child in PmName:
        if(pmcounter == child.text):
           list1.append(child.attrib)

print list1

record = open("record.csv","w")
PmData = Measurements.find('PmData')
for Pm in PmData:
    count = 0
    for key in list1:
        for child in Pm:
            if(child.attrib == key):
                value = child.text
                count += 1
                break;
        if (count != len(list1)):
            record.write(str(value)+",")
        else:
            record.write(str(value))
    record.write('\n')

record.close()