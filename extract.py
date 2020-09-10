import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from fitting import *

df = pd.read_table(r'.\data\stressLength.txt', header = 0, delim_whitespace = True)
dg = df[['frame','length','RF2']]
dr = dg.rename(columns = {'frame': 'Frame', 'length': 'Length', 'RF2':'Y-Resilience'})
dr = dr.astype(float)
print('Extract the complete, Data number: ', len(dr))
print(dr['Length'])
bilinear(dr['Length'], dr['Y-Resilience'])

x0 = np.linspace(0.2, 5, 100)
y0 = -9.0 * x0 ** 2 + 185
plt.plot(x0, y0, color = 'darkblue', linewidth = 2)

plt.xlim([0, 5])
plt.ylim([0, 200])
plt.xlabel('Crack Length/mm')
plt.ylabel('Stress/MPa')
plt.tight_layout()
plt.savefig(fname = r'.\figures\cracklength.pdf', format = 'pdf', transparent = False, dpi = 350, bbox_inches = 'tight')
plt.show()
