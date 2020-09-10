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
df = pd.read_table(r'.\data\stressU.txt', header = 0, delim_whitespace = True)
dg = df[['frame','stress','u']]
dr = dg.rename(columns = {'frame': 'Frame', 'stress': 'Stress', 'u':'Displacement'})
dr = dr.astype(float)
print('Extract the complete, Data number: ', len(dr))
# 生成子图对象
fig, ax = plt.subplots(figsize = (7,5))
dr.plot(kind = 'line', x = 'Displacement', y = 'Stress', ax = ax, color = 'darkblue', linewidth = 2)
ax.set_xlim([0, 0.0045])
ax.set_ylim([0, 200])
ax.set_xlabel('Displacement\mm')
ax.set_ylabel('Stress\MPa')
ax.legend().remove()
# 生成图像
plt.tight_layout()
plt.show()
fig.savefig(r'.\figures\dis_stress.pdf', transparent = False, dpi = 350, bbox_inches = 'tight')