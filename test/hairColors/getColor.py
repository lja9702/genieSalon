import cv2
import os
import numpy as np
import xml.etree.ElementTree as ET

def indent(elem, level=0): 
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i


mypath = "./"
ff = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

result = []

for f in ff:
  if f[-1] == 'g':
    img = cv2.imread(f, cv2.IMREAD_COLOR)
    m = [np.mean(img[:,:,0]), np.mean(img[:,:,1]), np.mean(img[:,:,2])]
    m = np.array(m).astype(int)
    result.append([m, f])


root = ET.Element("xml", kind="colors")
for i in result:
  color = ET.Element("color", name=i[1][:-4])
  r = ET.Element("r")
  r.text=str(i[0][2])
  g = ET.Element("g")
  g.text=str(i[0][1])
  b = ET.Element("b")
  b.text=str(i[0][0])
  color.append(r)
  color.append(g)
  color.append(b)
  root.append(color)

indent(root)
# create a new XML file with the results
ET.dump(root)
ET.ElementTree(root).write("color.xml")
