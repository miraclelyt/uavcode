# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:16:25 2019

@author: 01384599
"""

def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n
def _not_divisible(n):
    return lambda x: x % n > 0
def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列
for n in primes():
    if n < 1000:
        print(n)
    else:
        break
# In[]
def huishu(n):
    return n==int((str(n)[::-1]))
# In[]
def f_select(num):
    result = 0
    while num:
        tmp = num%10
        num = int(num / 10)
        result = result * 10 + tmp
    return result

def select(num):
    return f_select(num) == num
print(list(filter(select, range(1, 2000))))
# In[]
name=input()
classmate=['a','b','c']
len('classmate')
len(classmate)
print('I\'m OK')
print("I'm OK")
print('-\t-\\-\'-%-/-\n')
print(""" I can print ''' """)
print("""i
love
you""")
print(''' I can print """ ''')
print('''i
love
you''') #特殊功能,可以直接打印多行内容,而前面两种情况需要显示输入\n才能换行
print('''-\t-\\-\'-%-/-\n''') #可以看出还是和普通的字符串类似,会转义.
     # In[]
#打印出以下字符串
#n = 123
#f = 456.789
#s1 = 'Hello, world'
#s2 = 'Hello, \'Adam\''
#s3 = r'Hello, "Bart"'
#s4 = r'''Hello,
#Lisa!'''
print('''n = 123
f = 456.789
s1 = \'Hello, world\'
s2 = \'Hello, \\\'Adam\\\'\'
s3 = r\'Hello, \"Bart\"\'
s4 = r\'\'\'Hello,
Lisa!\'\'\'''')
# In[]
print('%2d-%02d'%(3, 1))
print('%.2f' % 3.1415926)
print('%03d%5d%.5f'%(1,2,3))
s1=72
s2=85
s=(s2-s1)/s1*100
print('小明成绩提升了%.2f%%'%s)

L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
]
print(L[0][0])
print(L[1][1])
# In[]
#小明身高1.75，体重80.5kg。请根据BMI公式（体重除以身高的平方）帮小明计算他的BMI指数，并根据BMI指数：
#•低于18.5：过轻
#•18.5-25：正常
#•25-28：过重
#•28-32：肥胖
#•高于32：严重肥胖

h=input('请输入小明身高(cm)：')
w=input('请输入小明体重(kg)：')
h=int(h)/100
w=int(w)
bmi=w/h**2
if bmi<18.5:
    print('过轻')
elif bmi>=18.5 and bmi<=25:
    print('正常')
else:
    print('过重')
    
L = ['Bart', 'Lisa', 'Adam']
for x in L:
    print('hello,',x)
for x in L:
    print('hello,%s'%x)#把空格去掉
    
n=0
while n < 10:
    n=n+1
    if n%2==0:
        break
    print(n)

d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
d['zdam']=80
d['list']='a list'

b=[1, 2, 3, 6]
s1 = set(b)
s2 = set([2, 3, 4, 5])
s3={1,2,3}
print(s1 & s2)
s1 | s2
#s2.add(b) 创建set需要list(也可以用大括号{}直接创建)，但是list不能加入到set中
s2
# In[]

def trim(s):
#    if s[len(s)-1]!=' ' & s[0]!=' ':
#        trim_s=s
    while s[-1:]==' ':
        s=s[0:-2]
    while s[:1]==' ':
        s=s[1:]
    return s
trim(s)
# In[]
def findmaxmin(a):
    max=a[0]
    min=a[0]
    for x in a:
        if x > max:
            max=x
        if x < min:
            min=x
    return(max,min)
findmaxmin(a)

# In[]
import os
[d for d in os.listdir('.')] 

# In[]
def fib(max):
    a,b,n=0,1,1
    while n < max:
#        print(b)
        yield b
        n+=1
        a,b=b,a+b
    return b
f=fib(8)
for n in f:
    print(n)
   # In[] 


def triangles():
    L=[1]
    yield L
    L=[1,1]
    n=2
    while True:
       yield L
       n=n+1
       A=L
       L=[1]
       for i in range(1,n-1):
         L.append(A[i-1]+A[i])
       L.append(1)
f=triangles()
   # In[] 
from functools import reduce
def f(x,y):
    a=10*x+y
    return a
reduce(f,[1,2,3,4,5])
   # In[] 
from functools import reduce
def prod(L):
    def muti(x,y):
        return x*y
    return reduce(muti,L)
prod({5,2,3,4,5})
prod([5,2,3,4,5])
prod((5,2,3,4,5))
   # In[] 
from functools import reduce
DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return DIGITS[s]
    return reduce(fn, map(char2num, s))
str2int('123455')
# In[] 
def str2float(s):
    DIGITS={'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '.' : '.'}
    def char2num(s):
        return DIGITS[s]
    def fn(x,y):
        return 10*x+y
    length=len(list(map(char2num,s)))
    l=length
    order=list(map(char2num,s)).index('.')
    o=order
    lis=list(map(char2num,s))
    del lis[order]
    print(lis)
    print(reduce(fn,lis))
    print(l)
    print(o)
    return (reduce(fn,lis))/(10**(l-o-1))
str2float('153.45676')    

# In[]
#筛选回数
#def fil(s):
#    l=[]
#    for n in len(str(s)):
#        while s!=0:
#            l.append(s%10)
#            s=(s-s%10)/10
#    for n in int(len(l)/2):
#        if l[n]==l[-(n+1)]:
            
#字符串可以直接切片引用        
def is_palindrome(n):
    return str(n)[:] == str(n)[::-1]
output = filter(is_palindrome, range(1, 1000))
print('1~1000:', list(output))
# In[]
#“闭包”的作用——保存函数的状态信息，使函数的局部变量信息依然可以保存下来
#闭包1:内部直接调用
def Maker(name):
    num=100
    def func1(weight,height,age):
        weight+=1
        height+=1
        age+=1
        print(name,weight,height,age)
    func1(100,200,300) #在内部就直接调用“内部函数”
Maker('feifei') #调用外部函数，输出 feifei 101 201 301

#闭包2:返回函数名称
def Maker(name):
    num=100
    def func1(weight,height,age):
        weight+=1
        height+=1
        age+=1
        print(name,weight,height,age)
    return func1 #此处不直接调用，而是返回函数名称（Python中一切皆对象）
maker=Maker('feifei') #调用包装器
maker(100,200,300) #调用内部函数


num=1
def a():
    global num
    num+=1
    print(num)
a()

def count():
    n=[0]
    def add():
        n[0]+=1
        print(n[0])
    return add
a=count()

def count():
    fs=[]
    for i in range(1,4):
        def f():
            return i*i
        fs.append(f)
    return fs
f1,f2,f3=count()
# In[]
f=lambda n:n%2==1
list(filter(f,range(1,20)))
# In[]
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
@log
def now():
    print('2015-3-25')
now.__name__

def log(func):
#    def wrapper(*args, **kw):
    print('call %s():' % func.__name__)
    return func
#    return wrapper
@log
def now():
    print('2015-3-25')
now.__name__ 

import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

import functools
def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args,**kw):
        print('%s executed in %s ms' % (fn.__name__, 10.24))
        return fn
    return wrapper
metric(now)
import time, functools
# In[]
#装饰器作业
import time, functools

def metric(fn):
    def wrapper(*args, **kw):
        startTime = time.time()
        fn(*args, **kw)
        endTime = time.time()
        gap = endTime - startTime
        print('%s executed in %s ms' % (fn.__name__, gap))
        return fn(*args, **kw)
    return wrapper

@metric
def fast(x, y):
    time.sleep(0.001)
#    return x + y

@metric 
def slow(x, y, z):
    time.sleep(0.1)
#    return x * y * z

f = fast(11, 22)
s = slow(11, 22, 33)
#if f != 33:
#    print('测试失败!')
#elif s != 7986:
#    print('测试失败!')

def v(func):
    print('权限验证')
    def wrap(*args,**kw):
        func(*args,**kw)
    return wrap
@v
def a():
    print('ok')
a()
# In[]
#偏函数
functools.partial(max,10)(2,3,15)
functools.partial(max,10)(2,3,5)
# In[]
import sys
sys.argv

if __name__=='__main__':
    print('__name__=',__name__)
# In[]
#类和实例    
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'
lisa = Student('Lisa', 99)
bart = Student('Bart', 59)
print(lisa.name, lisa.get_grade())
print(bart.name, bart.get_grade())

# In[]
#类和实例 
class Velocity():
    def __init__(self,vx,vy,vz):
        self.vx=vx
        self.vy=vy
        self.vz=vz
    def install(self):
        if abs(self.vx**2+self.vy**2+self.vz**2-18**2)<10:
            return('install')
        else:
            return('right')
a=Velocity(25,10,1)
print(a.install())

# In[]
class Animal():
    def run():
        print('Animal is running')
class Dog(Animal):
    def run():
        print('Dog is running')
def prin(animal):
    animal.run()
d=Dog()
prin(Animal)
prin(Dog)
type(d)
isinstance(d,Animal)
dir(d)
# In[]
class Student(object):
    count = 0
    def __init__(self, name):
        self.name = name
        Student.count += 1
        
s=Student('Bob')
s.name
s.count
s=Student('Bob1')
s.name
s.count

# In[]
class Student(object):
    pass
s = Student()
s.name = 'Michael' # 动态给实例绑定一个属性
print(s.name)

def set_age(self, age): # 定义一个函数作为实例方法
    self.age = age
    pass
from types import MethodType
s.set_age = MethodType(set_age, s) # 给实例绑定一个方法
s.set_age(25) # 调用实例方法
s.age # 测试结果

class Student(object):
    def __init__(self, age): # 定义一个函数作为实例方法
        self.age = age
s = Student(25)
s.age


class a():
    __slots__=('name','score')
    pass
b=a()
b.name='abc'
print(b.name)
b.add='abc'
print(b.add)

# In[]
class Screen(object):
    @property
    def height(self):
        return self.aheight
    @height.setter
    def height(self,value):
        if isinstance(value,int)==False:
            raise ValueError('score must be an integer!')
        if value>200 or value<30:
            raise ValueError('score must be an integer!!!')
        self.aheight=value
s=Screen()
s.height=60
s.height
# In[]
class Animal():
    pass
class Ani():
    pass
class Dog(Animal,Ani):
    pass
isinstance(Dog,Animal)
# In[]
class Student():
    def __init__(self,name):
        self.name=name
    def __str__(self):
        return 'Student name:%s' % self.name
#    __repr__=a
s=Student('ABC')
s
print(s)
# In[]
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def __str__(self):
        return '(%s: %s)' % (self.name, self.score)
    __repr__ = __str__

    def __cmp__(self, s):
        if self.name < s.name:
            return -1
        elif self.name > s.name:
            return 1
        else:
            return 0

s=Student('A',99)
# In[]
class Fib():
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
#    def __str__():
#        return a
#    __repr__=__str__
f=Fib()
# In[]
class Student(object):

    def __init__(self):
        self.name = 'Michael'

    def __getattr__(self, attr):
        if attr=='score':
            return 99
# In[]
#根据经纬度计算距离
import math
def geodistance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(math.radians, [float(lng1), float(lat1), float(lng2), float(lat2)]) # 经纬度转换成弧度
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2 
    distance=2*math.asin(math.sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=round(distance/1000,3)
    return distance
geodistance(113.5811347,22.3127046,113.6340863,22.2997324)
geodistance(114.7219828,26.0846054,114.7221717,26.0754419)
# In[]
from enum import Enum
a = Enum('b', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
a.Nov
type(a.Nov)
for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)

from enum import Enum, unique
@unique
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
type(Weekday)
type(Student)

# In[]
#GUI

import tkinter as tk

import tkinter.messagebox as mbox

# 定义MainUI类表示应用/窗口，继承Frame类

class MainUI(tk.Frame):

    # Application构造函数，master为窗口的父控件
    
    def __init__(self, master = None):
    
        # 初始化Application的Frame部分 
        
        tk.Frame.__init__(self, master)
        
        # 显示窗口，并使用grid布局
        
        self.grid()
        
        # 创建控件
        
        self.createWidgets()
        
        # 创建控件
    
    def createWidgets(self):
    
        # 创建一个标签，输出要显示的内容
        
        self.firstLabel = tk.Label(self,text="。")
        
        # 设定使用grid布局
        
        self.firstLabel.grid()
        
        # 创建一个按钮，用来触发answer方法
        
        self.clickButton = tk.Button(self,text="点一下瞧瞧？",command=self.answer)
        
        # 设定使用grid布局
        
        self.clickButton.grid()

    def answer(self):
    
        # 我们通过 messagebox 来显示一个提示框
        
        mbox.showinfo("哈哈哈",'''
        
        哈哈哈
        
        ''')


# 创建一个MainUI对象

app = MainUI()

# 设置窗口标题

app.master.title('「人人都是Pythonista」')

# 设置窗体大小

app.master.geometry('400x100')

# 主循环开始

app.mainloop()

# In[]
#GUI2
from tkinter import *           # 导入 Tkinter 库
root = Tk()                     # 创建窗口对象的背景色
                                # 创建两个列表
li     = ['C','python','php','html','SQL','java']
movie  = ['CSS','jQuery','Bootstrap']
listb  = Listbox(root)          #  创建两个列表组件
listb2 = Listbox(root)
for item in li:                 # 第一个小部件插入数据
    listb.insert(0,item)
 
for item in movie:              # 第二个小部件插入数据
    listb2.insert(0,item)
 
listb.pack()                    # 将小部件放置到主窗口中
listb2.pack()
root.mainloop()                 # 进入消息循环
# In[]
#GUI3
import tkinter as tk  # 使用Tkinter前需要先导入

# 第1步，实例化object，建立窗口window

window = tk.Tk()

# 第2步，给窗口的可视化起名字

window.title('My Window')

# 第3步，设定窗口的大小(长 * 宽)

window.geometry('500x300')  # 这里的乘是小x

# 第4步，在图形界面上设定输入框控件entry并放置控件

e1 = tk.Entry(window, show='*', font=('Arial', 14))   # 显示成密文形式

e2 = tk.Entry(window, show=None, font=('Arial', 14))  # 显示成明文形式

e1.pack()

e2.pack()

# 第5步，主窗口循环显示

window.mainloop()


# In[]
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox as mbox
# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('任务可行性评估')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('600x600')  # 这里的乘是小x
# 第4步，在图形界面上设定标签
l1 = tk.Label(window, text='总航程(km)', bg='grey', font=('Arial', 12), width=30, height=2)
e1 = tk.Entry(window, show=None, font=('Arial', 14))
l2 = tk.Label(window, text='固定翼爬升高度(m)', bg='grey', font=('Arial', 12), width=30, height=2)
e2 = tk.Entry(window, show=None, font=('Arial', 14))
l3 = tk.Label(window, text='固定翼下降高度(m)', bg='grey', font=('Arial', 12), width=30, height=2)
e3 = tk.Entry(window, show=None, font=('Arial', 14))
l4 = tk.Label(window, text='旋翼起飞高度(m)', bg='grey', font=('Arial', 12), width=30, height=2)
e4 = tk.Entry(window, show=None, font=('Arial', 14))
l5 = tk.Label(window, text='旋翼下降高度(m)', bg='grey', font=('Arial', 12), width=30, height=2)
e5 = tk.Entry(window, show=None, font=('Arial', 14))
# 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
# 第5步，放置标签m
l1.pack()    # Label内容content区域放置位置，自动调节尺寸
e1.pack()
l2.pack()
e2.pack()
l3.pack()
e3.pack()
l4.pack()
e4.pack()
l5.pack()
e5.pack()
float(e1.get())

# 创建一个按钮，用来触发answer方法
def Answer():
    
        # 我们通过 messagebox 来显示一个提示框
        
        mbox.showinfo("任务可行性评估",'''
        
        哈哈哈
        
        ''')
clickButton = tk.Button(text="11111",command=Answer)
# 设定使用grid布局
clickButton.pack()
# 放置lable的方法有：1）l.pack(); 2)l.place();
# 第6步，主窗口循环显示
window.mainloop()


from tkinter import * 
root=Tk()#定义StringVar()类对象
e=StringVar()
En=Entry(root,textvariable=e,state='readonly').pack()#对象值设定
e.set('Entry')#也可以像字典一样修改键对应的值#En['state']='readonly'
root.mainloop()

# In[]
try:
    print('try...')
    r = 10 / 0
    print('result:', r)
except ZeroDivisionError as e:
    print('except:', e)
finally:
    print('finally...')
print('END')



def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    bar('0')

main()


# In[]
from functools import reduce

def str2num(s):
    try:
        return int(s)
    except:
        return float(s)

def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    print(ss)
    return reduce(lambda acc, x: acc + x, ns)

def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 7.6')
    print('99 + 88 + 7.6 =', r)

main()


def abss(n):
    '''
    Function to get absolute value of number.
    
    Example:
    
    >>> abs(1)
    1
    >>> abs(-1)
    1
    >>> abs(0)
    0
    '''
    return n if n >= 0 else (-n)#注意这种写法
abss(-1)

# In[]
with open('d:/user/01384599/desktop/横市-大坪航线.kml','r',encoding='gbk',errors='ignore') as e:
    print(e.readlines())
with open('/Users/michael/test.txt', 'w') as f:
    f.write('Hello, world!')


# In[]
from io import StringIO
f=StringIO()
f.write('123')
print(f.getvalue())

from io import StringIO
f = StringIO('Hello!\nHi!\nGoodbye!')
# In[]
# StringIO和BytesIO

from io import BytesIO
# 实例化对象
byte_io = BytesIO()
byte_io.write("世界".encode("utf-8"))
# 全部读取
print(byte_io.getvalue().decode("utf-8"))


# In[]

import os
os.mkdir('D:\\user\\01384599\\desktop\\1')
os.rmdir('D:\\user\\01384599\\desktop\\1')
os.path.splitext('D:\\user\\01384599\\desktop\\11.txt')
os.path.split('D:\\user\\01384599\\desktop\\11.txt')

import shutil
[x for x in os.listdir('D:\\user\\01384599\\desktop')]
[x for x in os.listdir('D:\\user\\01384599\\desktop') if os.path.isfile(x) and os.path.splitext(x)=='.py']

# In[]
import json
obj = dict(name='小明', age=20)
json.dumps(obj, ensure_ascii=False)
json.dumps(obj)
# In[]
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
# if __name__ == '__main__' 我们简单的理解就是： 
# 如果模块是被直接运行的，则代码块被运行，如果模块是被导入的，则代码块不被运行。


# In[]
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(2)
    for i in range(3):
        p.apply_async(long_time_task, args=(i,))# 必要参数target:指定进程要执行的任务(这里是执行函数 action),必要参数args:直译成中文就是'参数'，顾名思义就是前面target的参数，即action的参数，注意args是个元组，所以args后的参数写成tuple元组格式。直接写target('进程一',0)一定报错的
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    
# In[]
import multiprocessing
import time

def action(a, b):  # 待会两个进程要执行的任务↓
    for i in range(30):  # 循环30次
        print(a, ' ', b)
        time.sleep(0.1)  # 等待0.1s

if __name__ == '__main__':  # 这行代码很重要，新建进程的时候都加上它！！原因不用管（我也不知道233）

    jc1 = multiprocessing.Process(target=action, args=('进程一', 0))  # 准备建立一个进程：multiprocessing.Process()
    jc2 = multiprocessing.Process(target=action, args=('进程二', 1))  # 再准备建立一个新进程，这是基本格式记住←
# 必要参数target:指定进程要执行的任务(这里是执行函数 action),必要参数args:直译成中文就是'参数'，顾名思义就是前面target的参数，即action的参数，注意args是个元组，所以args后的参数写成tuple元组格式。直接写target('进程一',0)一定报错的

    jc1.start()  # 将蓄势待发的jc1进程正式启动！！
    jc2.start()  # 同上...

    jc1.join()  # 等待进程jc1将任务执行完...
    jc2.join()  # ...
    print('jc1,jc2任务都已执行完毕')


# In[]
import time, threading

# 新线程执行的代码:
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)


# In[]
import os,multiprocessing
def run_process():
    print(111)
if __name__=='__main__':
    print('%s' % (os.getpid()))
    p=multiprocessing.Process(target=run_process)
    print('childproc %s will start ' %(os.getpid()))
    p.start()
    p.join()
    print('end')
    
# In[]
import subprocess

print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:', r)


# In[]

    
import time, threading

# 假定这是你的银行存款:
balance = 0

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
# In[]
#try finally
def test_finally_return1():
    try:
        print(1)
        return 1
    finally:
        print(0)
        return 0


def test_finally_return2():
    try:
        print(1)
        return 1
    finally:
        print(0)
        #return 0


def test_else_finally1():
    try:
        print(1)
        return 1
    except:
        return 2
    else:
        print(3)
        return 3
    finally:
        print(0)
        #return 0

def test_else_finally2():
    try:
        print(1)
        return 1
    except:
        return 2
    else:
        print(3)
        #return 3
    finally:
        print(0)
        return 0


def test_else_finally3():
    try:
        print(1)
        #return 1
    except:
        print(2)
        #return 2
    else:
        print(3)
        #return 3
    finally:
        print(0)
        return 0

def test_else_return1():
    try:
        print(1)
        return 1
    except:
        return 2
    else:
        print(3)
        return 3
    # finally:
    #     print(0)
        #return 0

def test_else_return2():
    try:
        print(1)
        #return 1
    except:
        return 2
    else:
        print(3)
        return 3
    # finally:
    #     print(0)
        #return 0


if __name__ == '__main__':
    print('测试1')
    print(test_finally_return1())
    print('测试2')
    print(test_finally_return2())
    print('测试3')
    print(test_else_finally1())
    print('测试4')
    print(test_else_finally2())
    print('测试5')
    print(test_else_return1())
    print('测试6')
    print(test_else_return2())
    print('测试7')
    print(test_else_finally3())
# In[]
import datetime
time=datetime.datetime.now()
print(time)

datetime.datetime(2016, 2, 29, 12, 20, 14).timestamp()


from collections import Counter
c = Counter('programming')
print(c)

c = Counter()
c.update('programming')
print(c)

Counter('programming')['m']
# In[]
from urllib import request

with request.urlopen('https://baidu.com/') as f:
    data = f.read()
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', data.decode('utf-8'))
# In[]
from turtle import *

# 设置笔刷宽度:
width(4)

## 前进:
#forward(100)
## 右转90度:
#right(144)

# 笔刷颜色:
for i in range(5):
    # 前进:
    forward(100)
    # 右转90度:
    right(144)
#pencolor('red')
#forward(100)
#right(144)
#
#pencolor('green')
#forward(100)
#right(144)
#
#pencolor('blue')
#forward(100)
#right(144)
#
#pencolor('grey')
#forward(100)
#right(144)
# 调用done()使得窗口等待被关闭，否则将立刻关闭窗口:
done()
# In[]

A=[{'name':'Bob','score':99},{'name':'AL','score':66}]
# In[]

def learn():
    print(1)
class Learn(object):
    def __init__(self,a):
        self.a=a
    def l(self):
        print(self.a)
    def __str__(self):
        return str(self.RangeCruise)
#    __repr__=__str__
s=Learn(2)
s.l
s.learn=learn
from types import MethodType
s.learn=MethodType(learn,s)
# In[]
#############################review
height=float(input('请输入身高（m）：'))
weight=float(input('请输入体重（kg）：'))
BMI=weight/height**2
##多种表达形式
if BMI < 18.5:
    print('您的BMI指数为%2.2f,过轻'%BMI)
elif BMI>=18.5 and BMI < 25:
    print('正常')
elif 25<=BMI < 28:
    print('过重')
elif BMI < 32:
    print('肥胖')
else:
    print('严重肥胖')
    
# In[]
#############################review
L = ['Bart', 'Lisa', 'Adam']
t=(1,2,3)
for x in L:
    print('hi,%s'%x)#没有逗号之后的空格

d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
d.get('Michael')

from math import sqrt
def qua(a,b,c):
    if (b**2-4*a*c)>=0:
        return (-b+sqrt(b**2-4*a*c))/2/a,(-b-sqrt(b**2-4*a*c))/2/a
    else:
        print('无实数解')
    
qua(1,-2,4)


def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)
enroll('a','b','c','d')

#######默认参数必须指向不变对象
def add_end(L=[]):
    L.append('end')
    return L
add_end()
add_end()

################################关键字参数
from functools import reduce
def product(*kw):
    return reduce(lambda x,y:x*y,kw)
product(1,2,3,4,5)
print('product(5) =', product(5))
print('product(5, 6) =', product(5, 6))
print('product(5, 6, 7) =', product(5, 6, 7))
print('product(5, 6, 7, 9) =', product(5, 6, 7, 9))
if product(5) != 5:
    print('测试失败!')
elif product(5, 6) != 30:
    print('测试失败!')
elif product(5, 6, 7) != 210:
    print('测试失败!')
elif product(5, 6, 7, 9) != 1890:
    print('测试失败!')
else:
    try:
        product()
        print('测试失败!')
    except TypeError:
        print('测试成功!')
################################递归函数
def move(n, a, b, c):

    if n==1:

        print(a, '- - >', c)

    else:

        move(n - 1, a, c, b)

        print(a, '- - >', c)

        move(n - 1, b, a, c)

move(2,'a','b','c')


# In[]
L1 = ['Hello', 'World', 18, 'Apple', None]
L2=[x.lower() for x in L1 if isinstance(x,str)]
print(L2)
if L2 == ['hello', 'world', 'apple']:
    print('测试通过!')
else:
    print('测试失败!')

# In[]

def triangles():
    
    yield line
    line=[1]+[line[i]+line[i+1] for i in range(len(line)-1)]+[1]
    
# 期待输出:
# [1]
# [1, 1]
# [1, 2, 1]
# [1, 3, 3, 1]
# [1, 4, 6, 4, 1]
# [1, 5, 10, 10, 5, 1]
# [1, 6, 15, 20, 15, 6, 1]
# [1, 7, 21, 35, 35, 21, 7, 1]
# [1, 8, 28, 56, 70, 56, 28, 8, 1]
# [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
n = 0
results = []
for t in triangles():
    results.append(t)
    n = n + 1
    if n == 10:
        break

for t in results:
    print(t)

if results == [
    [1],
    [1, 1],
    [1, 2, 1],
    [1, 3, 3, 1],
    [1, 4, 6, 4, 1],
    [1, 5, 10, 10, 5, 1],
    [1, 6, 15, 20, 15, 6, 1],
    [1, 7, 21, 35, 35, 21, 7, 1],
    [1, 8, 28, 56, 70, 56, 28, 8, 1],
    [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
]:
    print('测试通过!')
else:
    print('测试失败!')
    
    # In[]
def normalize(name):
#    name=name.lower()
    name=name.capitalize()
    return name

L1 = ['adam', 'LISA', 'barT']

L2 = list(map(str.capitalize, L1))

L2 = list(map(normalize, L1))
print(L2)


from functools import reduce
def prod(L):
    def cheng(x,y):
        return x*y
    return reduce(cheng,L)
print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')


# In[]
def is_palindrome(num):
    num=str(num)
    return num==num[::-1]
output = filter(is_palindrome, range(1, 1000))
print('1~1000:', list(output))
if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
    print('测试成功!')
else:
    print('测试失败!')

def a():
    fn=[]
    for x in range(1,4):
        def b():
            return x*x
        fn.append(b())
    return fn
f1, f2, f3 = a()

        
def a():
    fn=[]
    for x in range(1,4):
        def b():
            return x*x
        fn.append(b)
    return fn
f1, f2, f3 = a()



def createCounter():
    n=0
    def counter():
        nonlocal n
        n=n+1
        return n
    return counter
counterA = createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
counterB = createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')



