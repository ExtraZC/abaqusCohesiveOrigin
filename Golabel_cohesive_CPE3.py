# Function: 对inp文件进行操作,生成Cohesive单元
# Time: 190630
# Author: ZhangCheng
'''该程序使用应注意应将Fracture首先定义,单元号与节点号应从非断裂区开始'''

# 提取inp文件数据
ori_inp = open('Adaptivity-cohesive.inp', 'r')
Inp_line = ori_inp.readlines()

# 初始化
value = 0
k = 0
Node_dic = {}

for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Node'):
        value += 1
    if Inp_line[i].startswith('*Element'):
        value = 0
        break
    # 处理*Node~*Element之间的数据
    if value == 1:
        k += 1
        if k > 1:
            L = Inp_line[i].replace(' ', '').replace('\n', '').split(',')
            Node_dic[L[0]] = L[1:]
    else:
        pass
max_node = k - 1
print('Node_dic:', Node_dic)
print('max_node:', max_node)
# 读取开裂区与非开裂区的单元
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Elset, elset=Set-15, instance=PART-1-1, generate'):
        Fracture_start = int(Inp_line[i + 1].replace(' ', '').replace('\n', '').split(',')[0])
        Fracture_end = int(Inp_line[i + 1].replace(' ', '').replace('\n', '').split(',')[1])

print('开裂区单元: start end\n')
print('-----------', Fracture_start, '--', Fracture_end)

# 初始化
value = 0
Unfracture_dic = {}
Fracture_dic = {}
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Element'):
        k = 0
        value = 1
    if Inp_line[i].startswith('*Nset'):
        value = 0
        break
    if value == 1:
        k += 1
        if k > 1:
            ele = Inp_line[i].replace(' ', '').replace('\n', '').split(',')
            if int(ele[0]) in range(Fracture_start, Fracture_end + 1):
                Fracture_dic[ele[0]] = ele[1:]
    else:
        pass

print('Fracture_dic:', Fracture_dic)

Node_fracture_lis = []
for i in Fracture_dic:
    for j in Fracture_dic[i]:
        if j not in Node_fracture_lis:
            Node_fracture_lis.append(j)

print('Node Fracture list:', Node_fracture_lis)

Node_appeartimes = dict.fromkeys(Node_fracture_lis, 0)
for i in Fracture_dic:
    for j in Fracture_dic[i]:
        if j in Node_fracture_lis:
            Node_appeartimes[j] += 1
print('Fracture Node appeartimes:', Node_appeartimes)

New_Node_dic = {}

for i in Node_dic:
    if i not in Node_fracture_lis:
        New_Node_dic[i] = Node_dic[i]
    if i in Node_fracture_lis:
        for j in range(Node_appeartimes[i]):
            New_Node_dic[str(j * (10 ** (len(str(max_node)))) + int(i))] = Node_dic[i]

New_Node_assign = dict.fromkeys(New_Node_dic, 1)
New_Node_dic_sort = sorted([int(i) for i in New_Node_dic.keys()])
New_inp = open('New_inp.inp', 'w')

for i in range(len(Inp_line)):
    New_inp.write(Inp_line[i])
    if Inp_line[i].startswith('*Node'):
        break

for i in New_Node_dic_sort:
    New_inp.write(str(i))
    New_inp.write(', ')
    New_inp.write(New_Node_dic[str(i)][0])
    New_inp.write(', ')
    New_inp.write(New_Node_dic[str(i)][1])
    New_inp.write('\n')

def yu(x):
    if len(x) <= len(str(max_node)):
        return x
    if len(x) > len(str(max_node)):
        return str(int(x[-len(str(max_node)):]))
e = 0
for i in Fracture_dic:
    for j in range(len(Fracture_dic[i])):
        for k in New_Node_assign:
            if New_Node_assign[k] != 0 and yu(k) == Fracture_dic[i][j]:
                Fracture_dic[i][j] = k
                New_Node_assign[k] = 0
                e += 1
                New_inp.write(str(e))

for i in range(len(Inp_line)):
    if Inp_line[i].startswith('*Element, type=CPE3'):
        New_inp.write('*Element, type=CPE3\n')
        for j in range(Fracture_end - Fracture_start + 1):
            New_inp.write(str(Fracture_start + j))
            New_inp.write(', ')
            New_inp.write(Fracture_dic[str(Fracture_start + j)][0])
            New_inp.write(', ')
            New_inp.write(Fracture_dic[str(Fracture_start + j)][1])
            New_inp.write(', ')
            New_inp.write(Fracture_dic[str(Fracture_start + j)][2])
            # New_inp.write(', ')
            # New_inp.write(Fracture_dic[str(Fracture_start+j)][3])
            New_inp.write('\n')
        break
# 生成Cohesive单元
New_inp.write('*Element, type=COH2D4\n')
Cohesive_dic = {}
Fracture_dic_sort = sorted([int(i) for i in Fracture_dic.keys()])
k = Fracture_end + 1
for i in Fracture_dic_sort:
    for j in range(i + 1, Fracture_end + 1):
        l = []
        for m in Fracture_dic[str(i)]:
            for n in Fracture_dic[str(j)]:
                if yu(m) == yu(n):
                    l.append([m, n])
        if len(l) == 2:
            Cohesive_dic[str(k)] = [l[1][0], l[0][0], l[0][1], l[1][1]]
            k += 1
k1 = k
print("k1:",k1)
for i in range(Fracture_end + 1, k1):
    New_inp.write(str(i))
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][0])
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][1])
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][2])
    New_inp.write(', ')
    New_inp.write(Cohesive_dic[str(i)][3])
    New_inp.write('\n')

New_inp.close()
print("Insert successful")