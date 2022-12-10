import os.path
import sys
import xml.etree.cElementTree as ET
from xml.dom import minidom

"""
Before running this file download the stackoverflow data ( https://archive.org/download/stackexchange_20221005/stackoverflow.com-Posts.7z )
After downloading, provide the path in line 11
"""

path = os.path.join("D:\Santosh\stackoverflow.com-Posts", "Posts.xml")
# this line will create a file DataChunk.xml in the root folder of this file.
try:
    f = open('../data/posts_10000000.xml', 'x')
except:
    os.remove('../data/posts_10000000.xml')
    f = open('../data/posts_10000000.xml', 'w')
f.writelines('<?xml version="1.0" encoding="utf-8"?>')
f.write('\n')
f.writelines('<posts>')
# Get an iterable.
context = ET.iterparse(path, events=("start", "end"))

# the below for loop takes row by row from the large xml file and copy the row to DataChunk.xml
for index, (event, elem) in enumerate(context):
    # Get the root element.
    if index == 0:
        root = elem
    if event == "end":
        # ... process record elements ...
        try:
            xml_str = minidom.parseString(ET.tostring(elem)).toprettyxml()
            f.write(xml_str[22:])
        except:
            pass
        root.clear()
    file_size = os.stat('../data/posts_10000000.xml')
    print(file_size.st_size)
    # change according to your size. represents your data size in the bytes format.
    if file_size.st_size > 10000000:
        print(True)
        f.writelines("</posts>")
        sys.exit()
# 5368709120
