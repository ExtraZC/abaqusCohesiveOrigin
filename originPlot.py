# -*- coding: utf-8 -*-
'''
generate bilinear line chart from MD
'''
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# 使用ggplot默认样式
def form(route):
    plt.style.use('ggplot')
    mpl.rcParams['lines.linewidth']=2
    mpl.rcParams['axes.facecolor']='white'
    mpl.rcParams['axes.edgecolor']='black'
    mpl.rcParams['figure.dpi']=350
    mpl.rcParams['figure.figsize']=(8 / 2.54, 6 / 2.54)
    mpl.rcParams['savefig.dpi'] = 350
    mpl.rcParams.update({'font.size': 8})
    # Read Data
    df = pd.read_table(r'.\originData\0' + str(route) + '.txt', header = 0, delim_whitespace = True)
    dg = df[['xData','yData']]
    dr = dg.rename(columns = {'xData': 'X coord', 'yData': 'Y coord'})
    dr = dr.astype(float)
    return dr
    print('Extract the complete, Data number: ', len(dr))
# 生成子图对象
i0 = form(0)
i1 = form(1)
i2 = form(2)

fig, ax = plt.subplots(figsize = (7,5))
# color: firebrick darkblue forestgreen
# point: marker='.'
p0 = i0.plot(kind = 'line', x = 'X coord', y = 'Y coord', ax = ax, color = 'forestgreen', label = 'z direction')
p1 = i1.plot(kind = 'line', x = 'X coord', y = 'Y coord', ax = ax, color = 'darkblue', label = 'y direction')
p2 = i2.plot(kind = 'line', x = 'X coord', y = 'Y coord', ax = ax, color = 'firebrick', label = 'x direction')

ax.set_xlim([0, 0.2])
ax.set_ylim([0, 16])
# ax.axis['bottom'].set_axis_direction('top')
ax.set_xlabel('Strain')
ax.set_ylabel('Stress')
legend = ax.legend((p0, p1, p2))
frame = legend.get_frame()
ax.legend(loc = 1, frameon = False)
frame.set_facecolor('none')
# 生成图像
plt.tight_layout()
plt.show()
fig.savefig(r'.\figures\.pdf', transparent = False, dpi = 350, bbox_inches = 'tight')


