from abaqus import *
from abaqusConstants import *
import visualization as vis

# 创建窗口视图, 通过Viewport函数, 名称(name)
myViewport = session.Viewport(name='Superposition example',origin=(10,10),width=100,height=100)
# 打开已经存在的odb结果文件, 通过path指定odb文件
myOdb = vis.openOdb(path='C:\\Users\\ZhangC\\test.odb')
# 在当前视图窗口显示结果对象, 设置默认的plot对象
myViewport.setValues(displayedObject=myOdb)
# 创建一个载荷步对象
firstStep = myOdb.steps['Step-1']
# 创建两个帧对象, -1表示最后一帧
frame1 = firstStep.frames[-1]
frame2 = firstStep.frames[-5]
# 选取两个载荷步最后一帧的位移场
dis1 = frame1.fieldOutputs['U']
dis2 = frame2.fieldOutputs['U']
# 选取两个载荷步最后一帧的应力场
stress1 = frame1.fieldOutputs['S']
stress2 = frame2.fieldOutputs['S']
# 创建新的输出场
deltaDis = dis1 - dis2
deltaStress = stress1 - stress2
# 设置形状变形, 依据新的位移场, Abaqus通过这个变量来显示变形形状
myViewport.odbDisplay.setDeformedVariable(deltaDis)
# 创建新的应力场云图, 场数据是新的应力场, 输出位置是积分点, 显示其中的Mises应力
myViewport.odbDisplay.setPrimaryVariable(field = deltaStress, outputPosition=INTEGRATION_POINT, refinement = (INVARIANT,'Mises'))
# 显示新的Mises云图, 并且在变形后的图形上显示
myViewport.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF,))