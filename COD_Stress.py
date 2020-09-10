# -*- coding: utf-8 -*-
'''
Generate COD and Stress related data.
'''
from odbAccess import *
import numpy as np
# 提取Odb文件
odb = openOdb(r'D:\Users\tiany\OneDrive\Git\Self\Serious\paper\firstData\abaqus\Voronoi\grain70\edge02\grainedge02.odb')
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
# 保存数据
sav = []
stressCOD = open(r'D:\Users\tiany\OneDrive\Git\Self\Serious\paper\firstData\program\Grain\data\stressCOD', 'w')
# stressData.write('   frame           length           s11             s22            s33              s12             Inv3         maxInPlanePri     maxPrin         midPrin        minInPlanePrin     minPrin         mises            tresca    ')
stressCOD.write('frame  COD  Stress')
stressCOD.write('\n')
stressCOD.close()
# x轴判断
minCoordX = 0
# 生成odb对象
assembly = odb.rootAssembly
instance = assembly.instances['TESS']
# 所有节点集
node = instance.nodes
step1 = odb.steps['Step-1']
frame = step1.frames
# 第0帧
# 支反力集合
rfNode = assembly.nodeSets['SET-5']
j = 1 # 内聚力集名称
label = 1 # 内聚力单元编号

for i in range(len(frame)):
    # 获取内聚力单元集
    bound = 'BOUND' + str(j)
    cohesive = instance.elementSets[bound]  # 内聚力单元集
    sdegElement = cohesive.elements  # 损伤单元集
    length = 0  # 初始化裂纹长度
    # 获取载荷施加点的支反力
    rfField = frame[i].fieldOutputs['RF']
    fieldRf = rfField.getSubset(region=rfNode)
    rfValue = fieldRf.values
    Rf2 = rfValue[0].data[1]
    # 获取cohesive损伤单元
    stressField = frame[i].fieldOutputs['S']
    Stress =
    sdeg = frame[i].fieldOutputs['SDEG']
    # 得到cohesive区域的子集
    fieldSdeg = sdeg.getSubset(region=cohesive, position=INTEGRATION_POINT)
    fieldStress = stressField.getSubset(region=cohesive, position=INTEGRATION_POINT)
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
    # 得到每一帧中损伤单元的每个长度
    for g in dNode:
        for h in range(1, len(dNode[g])):
            if dCoord[dNode[g][0]][1] == dCoord[dNode[g][h]][1]:
                COD += np.sqrt(np.square(dCoord[dNode[g][h]][1] - dCoord[dNode[g][0]][1]) + np.square(dCoord[dNode[g][h]][2] - dCoord[dNode[g][0]][2]))
    print 'frame, length, Rf2: ', i, COD, Stress
    sav.append([i, COD, Stress])
# 保存数据
stressCODArray = np.array(sav)
with open(r'D:\Users\tiany\OneDrive\Git\Self\Serious\paper\firstData\program\Grain\data\stressCOD\stressCOD70.txt','ab') as f:
    np.savetxt(f, stressCODArray, fmt='%f', delimiter='  ')
print 'Extract Complete'