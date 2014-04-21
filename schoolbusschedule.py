from tkinter import tix
from tkinter import *
from time import strftime
import sqlite3 as dbapi
import os

import scheduleDB

'''对相应组件进行布局，并进行简单的事件响应，显示数据'''
window = Tk()
#校车时间查询
window.title('Bus_Time_Schedule')
window.minsize(360,320)
window.maxsize(360,320)

frame = Frame(window)
frame.pack()

#共东西南北四个站台
stations = ['东区北门','西区图书馆','南区图书馆','北区门口']

def omchanged(event):
    '清空内容,END为结尾标记'
    printResult()
def cbchanged():
    printResult()

src = StringVar(frame)
src.set(stations[1])
sl = Label(frame, text="起始站：")
sl.grid(row=0,column=0)
so = OptionMenu(frame, src, *stations, command=omchanged)
so.grid(row=0,column=1)

el = Label(frame, text="终点站：")
el.grid(row=1,column=0)
dst = StringVar(frame)
dst.set(stations[0])
do = OptionMenu(frame, dst, *stations, command=omchanged)
do.grid(row=1,column=1)

#记录是否从当前时间开始查询
cbVar1 = IntVar()
C1 = Checkbutton(frame, text = "从当前开始查询", variable = cbVar1,
                 onvalue = 1, offvalue = 0, height=1,
                 width = 10, command=cbchanged)
C1.grid(row=2,column=1)
#默认选中
C1.select()

#记录是否为节假日
cbVar2 = IntVar()
C2 = Checkbutton(frame, text = "现在是节假日", variable = cbVar2,
                 onvalue = 1, offvalue = 0, height=1,
                 width = 10, command=cbchanged)
C2.grid(row=2,column=0)

def printResult():
    lb.delete(0,END)
    sql = "SELECT *  from schedule where "
    sql += (" dst='"+dst.get().strip()+"'")
    sql += (" and src='"+src.get().strip()+"'")
    cb2Value = cbVar2.get()
    '根据Checkbutton 获取当前是否为节假日'
    if cb2Value == 1:
        sql += (" and state='1'")
    sql += " and time>'"    
    cb1Value = cbVar1.get()
    '根据Checkbutton 获取小时：分钟'
    if cb1Value == 0:
        sql += ("00:00'")
    elif cb1Value == 1:
        sql += (strftime("%H:%M")+"'")
    sql += " order by time ASC "

    '连接数据库'
    con = dbapi.connect('schedule.db')
    cur = con.cursor()
    cur.execute(sql)
    '获取结果'
    results = cur.fetchall()
    #print(sql)
    #print(results)
    con.close()
    if len(results) > 0:
        rt = ''
        for att in ['班次','假日正常','时间','起点','终点']:
            rt += (att+'    ')
        lb.insert(END,rt+'\n')
    for reslut in results:
        rt = ''
        for att in reslut:
            rt += (att+'  ')
        lb.insert(END,rt+'\n')
    #print(strftime("%Y-%m-%d %H:%M:%S")+' '+src.get()+'->'+dst.get())
#search = Button(frame,text="查询班次",command=printResult)
#search.grid(row=1,column=2)

var = StringVar()
lb = Listbox(frame, height=12, selectmode=BROWSE, width=48, listvariable = var)
scrl = Scrollbar(frame)
scrl.grid(row=3,column=3)
lb.grid(row=3,column=0,columnspan=3)
#lb.pack(side=LEFT, fill=BOTH)
scrl['command'] = lb.yview

'默认执行一次'
printResult()

window.mainloop()
