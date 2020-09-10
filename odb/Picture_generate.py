# -*- coding: utf-8 -*-
'''
Reading Data, generate Stress-U related line chart
'''
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# from IPython.core.pylabtools import figsize
# from matplotlib.ticker import MultipleLocator, FuncFormatter
# import numpy as np

# 设置自定义x,y的label
# def currency(y, pos):
#     if y >= 100:
#         return '{:1.0f}GPa'.format(y*1e-3)
#     return '{:1.0f}MPa'.format(y*1)

# 初始化
data_dic = {}
fram_dic = {}
k = 0
# 读取文件
# header = None: delim_whitespace = True: 用空格来分隔每行的数据, index_col=0:设置第1列数据作为index
ori_file = open('D:\\Users\\ZhangC\\PycharmProjects\\Job2_inp\\odb\\ODB_Data\\stressU.txt','r')
Inp_line = ori_file.readlines()

for i in range(len(Inp_line)):
    L = Inp_line[i].replace('\n','').split()
    data_dic[i] = L

for i in data_dic[0]:
    fram_dic[i] = []

for i in fram_dic:
    for j in range(1, len(data_dic)):
        fram_dic[i].append(data_dic[j][k])
    if k <= len(fram_dic):
        k += 1
    else:
        k = 0
# 使用ggplot默认样式
plt.style.use('ggplot')
# 使用rcParams设置全局参数
mpl.rcParams['lines.linewidth']=2
mpl.rcParams['axes.facecolor']='white'
mpl.rcParams['axes.edgecolor']='black'
mpl.rcParams['figure.dpi'] = 350
mpl.rcParams['figure.figsize'] = (8 / 2.54, 6 / 2.54)
mpl.rcParams['savefig.dpi'] = 350
mpl.rcParams.update({'font.size': 8})
# 获取数据
df = pd.DataFrame(fram_dic)
dg0 = df[['frame', 'stress', 'u']]
dr0 = dg0.rename(columns = {'frame': 'Frame', 'stress': 'Stress', 'u': 'U'})
dr0 = dr0.astype(float)
print('Extract the complete, Data number: ', len(df))
# 生成子图对象
fig, ax = plt.subplots(figsize = (7,5))
# 颜色多采用: darkblue, firebrick, seagreen
dr0.plot(kind = 'line', x = 'U', y = 'Stress', ax = ax, color = 'darkblue')
# 设置子图对象参数
ax.set_xlim([0, 0.0045])
ax.set_ylim([0, 200])
ax.set_xlabel('Displacement')
ax.set_ylabel('Stress')
# ax.legend().set_visible(False)
# 使用自定义label格式
# formatter = FuncFormatter(currency)
# ax.yaxis.set_major_formatter(formatter)
# 紧凑布局
plt.tight_layout()
plt.show()
fig.savefig('D:\\Users\\ZhangC\\PycharmProjects\\Job2_inp\\odb\\ODB_Data\\Rf_Displacement.pdf', transparent = False, dpi = 350, bbox_inches = 'tight')