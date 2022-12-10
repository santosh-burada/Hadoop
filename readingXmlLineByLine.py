import os.path
import sys
import xml.etree.cElementTree as ET
from xml.dom import minidom

path = os.path.join("D:\Santosh\stackoverflow.com-Posts", "Posts.xml")
# tree = ET.parse(path)
# root = tree.getroot()
# print(root)
# c=0
# for ele in root:
#     c+=1
#     print(c)
# print(c)
f = open('test.xml', 'a')

# Get an iterable.
context = ET.iterparse(path, events=("start", "end"))
print("reading done")
# print(context)
for index, (event, elem) in enumerate(context):
    # Get the root element.
    if index == 0:
        root = elem

    if event == "end":
        # ... process record elements ...
        print(index)
        try:
            xmlstr = minidom.parseString(ET.tostring(elem)).toprettyxml()
            f.write(xmlstr[22:])
        except:
            pass
        root.clear()
    file_size = os.stat('test.xml')
    if file_size.st_size == 5368709120:
        sys.exit()
