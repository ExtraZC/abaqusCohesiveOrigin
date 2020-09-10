# -*- coding: utf-8 -*-
'''
Reading "SDEG" element generate Crack-Length and Stress related data.
'''
# 读取odb文件
from odbAccess import *
import numpy as np
# 提取inp文件数据
ori_inp = open(r'grainedge02.inp', 'r')
Inp_line = ori_inp.readlines()
# 初始化
value = 0
k = 0
# 判断节点最大位数
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Nset, nset=SET-1, generate'):
        max_node = Inp_line[i+1].replace(' ','').replace('\n','').split(',')[1]
print 'Max_node: ', max_node
ori_inp.close()
# 比较新增节点与旧节点
def yu(x):
    if len(x) <= len(max_node):
        return x
    if len(x) > len(max_node):
        return str(int(x[-len(max_node):]))
# 获取Odb文件
odb = openOdb(r'C:\Users\ZhangC\TiAl_cohesive_True.odb')
# 最大单元
dElement = {}
label = []
# 损伤单元节点集
dNode = {}
# 每一帧中损伤最大坐标
dCoord = {}
maxCoord = []
# 每一帧中损伤最小坐标
minCoord = []
# 创建数据文件
sav = []
stressLength = open(r'D:\Users\ZhangC\PycharmProjects\Job2_inp\odb\ODB_Data\stressLength.txt', 'w')
stressLength.write('frame  length  RF2')
stressLength.write('\n')
stressLength.close()
# 生成odb对象
assembly = odb.rootAssembly
instance = assembly.instances['PART-1-1']
# 内聚力单元集
cohesive = instance.elementSets['COHESIVE']
# 所有节点集
node = instance.nodes
step1 = odb.steps['Step-1']
frame = step1.frames
# 损伤单元对象
sdegElement = cohesive.elements
rfNode = assembly.nodeSets['SET-9']

for i in range(len(frame)):
    # 裂纹长度
    length = 0
    # 获取载荷施加点的支反力
    rfField = frame[i].fieldOutputs['RF']
    fieldRf = rfField.getSubset(region=rfNode)
    rfValue = fieldRf.values
    Rf2 = rfValue[0].data[1]
    # 获取cohesive损伤单元
    stressField = frame[i].fieldOutputs['S']
    sdeg = frame[i].fieldOutputs['SDEG']

    # 得到cohesive区域的子集
    fieldSdeg = sdeg.getSubset(region = cohesive, position = INTEGRATION_POINT)
    fieldStress = stressField.getSubset(region = cohesive, position = INTEGRATION_POINT)
    # TODO 该处可以更改为COD的数据获取
    # 得到损伤单元的编号
    for fs in range(len(fieldSdeg.values)-1):
        # FIXME 损伤单元的判定条件有误
        # FIXME 已经查明该单元的损伤判定由data(其值最大为预先设置的损伤值)负责
        if fieldSdeg.values[fs].data > 0.99 and fieldSdeg.values[fs].elementLabel not in label:
            label.append(fieldSdeg.values[fs].elementLabel)
    print 'label: ', label
    # 得到损伤单元的节点
    for l in label:
        for se in range(len(sdegElement) - 1):
            if sdegElement[se].label == l:
                dNode[l] = sdegElement[se].connectivity
    print 'dNode: ', dNode
    # 得到损伤单元的节点的坐标
    for dn in dNode:
        for h in dNode[dn]:
            for j in range(len(node) - 1):
                if node[j].label == h:
                    dCoord[h] = [dn, node[j].coordinates[0], node[j].coordinates[1], node[j].coordinates[2]]
    print 'dCoord: ', dCoord
    # minidCoord = minCoord
    # FIXME maxCoord 与 minCoord的坐标赋值因为载体的中间会出现失效单元, 所以在30帧会使得最大坐标判定失效
    # TODO 在每帧的失效单元的两两不同的节点的距离进行计算, 进行sum得出每帧的裂纹长度, 这种想法是可行的
    # 得到每一帧中损伤单元的每个长度
    for g in dNode:
        for h in range(1, len(dNode[g])):
            if yu(str(dNode[g][0])) != yu(str(dNode[g][h])):
                length += np.sqrt(np.square(dCoord[dNode[g][h]][1]-dCoord[dNode[g][0]][1])+np.square(dCoord[dNode[g][h]][2]-dCoord[dNode[g][0]][2]))
    print 'frame, length, Rf2: ', i, length, Rf2
    sav.append([i, length, Rf2])
# 保存数据
stressLengthArray = np.array(sav)
with open(r'D:\Users\ZhangC\PycharmProjects\Job2_inp\odb\ODB_Data\stressLength.txt','ab') as f:
    np.savetxt(f, stressLengthArray, fmt='%f', delimiter='  ')
print 'Extract Complete'