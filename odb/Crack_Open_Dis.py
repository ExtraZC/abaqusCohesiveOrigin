# -*- coding: utf-8 -*-
'''
Generate COD and Stress related data.
'''
from odbAccess import *
import numpy as np
# 提取Odb文件
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
# 保存数据
sav = []
stressCOD = open('D:\Users\ZhangC\PycharmProjects\Job2_inp\odb\ODB_Data\stressCOD.txt', 'w')
# stressData.write('   frame           length           s11             s22            s33              s12             Inv3         maxInPlanePri     maxPrin         midPrin        minInPlanePrin     minPrin         mises            tresca    ')
stressCOD.write('frame  COD  RF2')
stressCOD.write('\n')
stressCOD.close()
# x轴判断
minCoordX = 0
# 第0帧
sdeg0 = frame[0].fieldOutputs['SDEG']
fieldSdeg0 = sdeg0.getSubset(region = cohesive, position = INTEGRATION_POINT)
for i in range(len(fieldSdeg0.values)-1):
    elementLabel = fieldSdeg0.values[i].elementLabel
    for j in range(len(node)-1):
        if node[j].label == elementLabel and node[j].coordinates[1] == 0:
            if node[j].coordinates[0] < minCoordX:
                minCoord = [node[j].coordinates[0], 0]
minCoord = [-0.7, 0]
print 'minimum X coord(when Y=0): ', minCoord

for i in range(len(frame)):
    # 得到每一帧中损伤单元中x轴最远的坐标和单元号
    for g in dCoord:
        if dCoord[g][1] >= minidCoord[0] and len(dCoord) > 0:
            maxCoord = [dCoord[g][1], dCoord[g][2]]
            minidCoord = [dCoord[g][1], dCoord[g][2]]
            maxLabel = dCoord[g][0]
    # 得到最大损伤单元的相关数据, 比如应力, 应力分量
    if length > 0:
        print 'maxCoordX, maxCoordY, minCoordX, minCoordY: ', maxCoord[0], maxCoord[1], minCoord[0], minCoord[1]
        minCoord = maxCoord
        for j in range(len(fieldStress.values) - 1):
            h = fieldStress.values[j]
            if h.elementLabel == maxLabel:
                sCom = [h.data[0], h.data[1], h.data[2], h.data[3]]
                s11 = h.data[0]
                s22 = h.data[1]
                s33 = h.data[2]
                s12 = h.data[3]
                sInv3 = h.inv3
                sMaxInPlane = h.maxInPlanePrincipal
                sMaxPrinc = h.maxPrincipal
                sMidPrinc = h.midPrincipal
                sMinInPlane = h.minInPlanePrincipal
                sMinPrinc = h.minPrincipal
                sMises = h.mises
                sTresca = h.tresca
        sav.append([i, length, s11, s22, s33, s12, sInv3, sMaxInPlane, sMaxPrinc, sMidPrinc, sMinInPlane, sMinPrinc, sMises, sTresca])
        print 'sav:', sav
