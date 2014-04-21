import sqlite3 as dbapi
import os
import os.path as path
from time import strftime

'''将班次数据写入schedule.db文件，共主程序查询数据库显示数据'''

enkeys = ['type', 'state' 'time', 'src', 'dst']
chkeys = []
values = []
sqls = []

if path.exists("schedule.db"):
    os.remove("schedule.db")
con = dbapi.connect('schedule.db')
cur = con.cursor()
cur.execute('CREATE TABLE schedule(type TEXT, state TEXT, time TEXT, src TEXT, dst TEXT)')

#读文件并将相应数据记入chkeys和values列表中
r = open("schedule.txt","r")
line = r.readline()
for att in line.strip(' \n').split():
    chkeys.append(att)
line = r.readline()
for line in r:
    value = line.strip(' \n').split()
    values.append(value)
r.close()   
#生成sql语句
for value in values:
    sql = 'INSERT INTO schedule VALUES('
    for att in value:
        sql += ('"'+att+'"' + ',')
    sqls.append(sql[:-1]+')')
#执行插入数据动作
for sql in sqls:
    cur.execute(sql)

con.commit()
##print(strftime("%H:%M"))
#cur.execute("SELECT *  from schedule")
##cur.execute("SELECT *  from schedule where dst='西区图书馆' and src='东区北门' and time>'"+strftime("%H:%M")+"'")
##cur.execute("SELECT *  from schedule where dst='东区北门' and src='西区图书馆' and time>'00:00'")
##print(enkeys)
##print(chkeys)
##print(values)
##print(sqls)
##print(cur.fetchall())
con.close()
