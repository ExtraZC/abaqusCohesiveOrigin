# -*- coding: utf-8 -*-
'''
Reading Applying displacement generate Resilience and displacement, output among the relation.
'''
from odbAccess import *
import numpy as np

odb = openOdb(r'C:\Users\ZhangC\TiAl_cohesive_True.odb')

stressU = open('D:\Users\ZhangC\PycharmProjects\Job2_inp\odb\ODB_Data\stressU.txt', 'w')
stressU.write('frame      stress       u')
stressU.write('\n')
stressU.close()

sav = []

assembly = odb.rootAssembly
instance = assembly.instances['PART-1-1']
node = assembly.nodeSets[' ALL NODES'].nodes[1]
step1 = odb.steps['Step-1']
frame = step1.frames
rfNode = assembly.nodeSets['SET-9']

for i in range(len(frame)):
    # 获取载荷施加点的支反力
    rfField = frame[i].fieldOutputs['RF']
    fieldRf = rfField.getSubset(region=rfNode)
    rfValue = fieldRf.values
    Rf2 = rfValue[0].data[1]
    # 获取载荷施加点的位移
    disField = frame[i].fieldOutputs['U']
    fieldDis = disField.getSubset(region = rfNode)
    disValue = fieldDis.values
    Dis2 = disValue[0].data[1]
    print 'frame, Rf2, Dis2: ', i, Rf2, Dis2
    sav.append([i, Rf2, Dis2])
rfDis = np.array(sav)
with open('D:\Users\ZhangC\PycharmProjects\Job2_inp\odb\ODB_Data\stressU.txt','ab') as f:
    np.savetxt(f, rfDis, fmt = '%f', delimiter = '  ')
print 'Extract Complete'
