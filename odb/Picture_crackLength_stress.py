# -*- coding: utf-8 -*-
'''
Reading Data, generate related line chart
'''
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# 使用ggplot默认样式
plt.style.use('ggplot')
mpl.rcParams['lines.linewidth']=2
mpl.rcParams['axes.facecolor']='white'
mpl.rcParams['axes.edgecolor']='black'
mpl.rcParams['figure.dpi']=350
mpl.rcParams['figure.figsize']=(8 / 2.54, 6 / 2.54)
mpl.rcParams['savefig.dpi'] = 350
mpl.rcParams.update({'font.size': 8})
# Read Data
df = pd.read_table('D:\\Users\\ZhangC\\PycharmProjects\\Job2_inp\\odb\\ODB_Data\\stressLength.txt', header = 0, delim_whitespace = True)
dg = df[['frame','length','RF2']]
dr = dg.rename(columns = {'frame': 'Frame', 'length': 'Length', 'RF2':'Y-Resilience'})
dr = dr.astype(float)
print('Extract the complete, Data number: ', len(dr))
# 生成子图对象
fig, ax = plt.subplots(figsize = (7,5))
dr.plot(kind = 'line', x = 'Length', y = 'Y-Resilience', ax = ax, color = 'firebrick')
ax.set_xlim([0, 5])
ax.set_ylim([0, 190])
ax.set_xlabel('CrackLength')
ax.set_ylabel('Y-Resilience')
# 生成图像
plt.tight_layout()
plt.show()
fig.savefig('D:\\Users\\ZhangC\\PycharmProjects\\Job2_inp\\odb\\ODB_Data\\length_stress.png', transparent = False, dpi = 350, bbox_inches = 'tight')