import sys

'''需要在命令行中执行，从命令行参数中提到的多个文件中按指定格式提取出'班次数据'
并写入到'schedule.txt'文件供schduleDB.py将班次数据写入数据库'''
chkeys = []
values = []
for file in sys.argv[1:]:
    r = open(file,'r')
    line = r.readline()
    #暂记班次类别
    tp = line.strip(' \n')  
    line = r.readline()
    #中文站台名称
    chkey = line.strip(' \n').split()
    #将班次类别插入chkey第一个位置
    chkey.insert(0,tp)
    chkeys.append(chkey)
    for line in r:
        #记录站台对应的出发时间
        value = line.strip(' \n').split()
        value.insert(0,tp)
        values.append(value)
print(chkeys)
print(values)
print(len(chkeys))
print(len(values))

w = open('schedule.txt','w')
#正常表示节假日是否仍正常运行，1为是0为否
w.write('%10.6s%10.6s%10.6s%10.6s%10.6s\n' % ('班次','正常','时间','起点','终点'))

for value in values:
    for chkey in chkeys:
        if value[0] != chkey[0]:
            continue
        else:
            '去除重复的班次记录，保证每条班次记录唯一'
            start_to_end = []
            for m in range(2, len(chkey)):
                for n in range(m+1, len(value)):
                    if (value[m],chkey[m],chkey[n]) not in start_to_end and chkey[m] != chkey[n]:
                        start_to_end.append((value[m],chkey[m],chkey[n]))
                        '处理异常情况，将7:38改为07:38'
                        if(len(value[m]) == 4):
                            w.write('%10.6s%10.6s%10.6s%10.6s%10.6s\n' % (value[0],value[2], "0"+value[m],chkey[m],chkey[n]))
                        elif(len(value[m]) == 5):
                            w.write('%10.6s%10.6s%10.6s%10.6s%10.6s\n' % (value[0],value[2], value[m], chkey[m], chkey[n]))
w.close()
