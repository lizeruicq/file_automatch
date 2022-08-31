import os
import tkinter
import shutil
from fnmatch import fnmatch
import threading
import datetime
import windnd

def pathfy(path,name):
    return os.path.join(path,name)

def namefy(path):
    return os.path.basename(path)

def check(path):
    return os.path.exists(path)


def gettime():
    curr_time = datetime.datetime.now()
    curr_time=datetime.datetime.strftime(curr_time, '%H-%M-%S')
    return curr_time

#特殊位置匹配
def match_special(file,dir):
    temp = dir.split(' ')
    # print(temp[-1])
    if fnmatch(file,'*'+temp[-1]+'*'):
        return True
    elif ('CHS' in file or 'CHT' in file) and (dir == 'CHT&CHS'):
        return True
    else:
        return False
def match_rules(src,dir):
    if fnmatch(namefy(src), '*' + dir + '*'):
        return True
    elif  match_special(namefy(src),dir):
        return  True
    else:
        return False


#src为图片的路径，pos为当前路径， list1为子目录的路径
def movepic(origin,src,pos,list1):
    #所有子目录的名称
    time = gettime()
    list2 = [namefy(i) for i in list1]
    for dir in list2:
        if match_rules(src,dir):
        # if fnmatch(namefy(src), '*' + dir + '*') or match_special(namefy(src),dir):
            print(namefy(src)+'与'+dir+'匹配成功')
            nextpos = os.path.join(pos,dir)
            if check(os.path.join(nextpos,os.path.basename(src))):
                print('目录存在同名文件'+namefy(src)+'，将文件移动回初始位置')
                shutil.move(src,origin)
                break
            shutil.move(src, nextpos)
            print(src + "移动到----->" + nextpos)
            pos = nextpos
            src = os.path.join(pos,os.path.basename(src))
            nextlist = scandir(pos)
            movepic(origin,src, pos, nextlist)
            with open('log'+ time +'.txt','at') as f:
                if check(src):
                    f.write(src + '\n')
            break
        else:
            print(namefy(src) + '与' + dir + '名称不匹配,跳过')
            continue

def scandir(path):
    filelist = os.listdir(path)
    filelist = [os.path.join(path,i) for i in filelist]
    candidates = [os.path.join(path,name) for name in filelist if os.path.isdir(name)]
    return candidates

def scanfile(path):
    filelist = os.listdir(path)
    filelist = [os.path.join(path, i) for i in filelist]
    candidates = [os.path.join(path, name) for name in filelist if os.path.isfile(name)]
    return candidates

# def createlog():
#     with open('lastlog.txt','wt') as f:
#         for i in destination:
#             f.write(str(i))

#社群在多语言的子目录下再次创建与父目录名称相同的目录
def makecopydir(src,targ):
    langs = []
    src_list = [namefy(i) for i in scanfile(src)]
    targ_list = [namefy(i) for i in scandir(targ)]
    for i in targ_list:
        for j in src_list:
            if match_rules(j,i):
            # fnmatch(j , '*'+i+'*') or match_special(j,i):
                if i not in langs:
                    langs.append(i)
    if langs!=[]:
        for k in langs:
            newdir = pathfy(targ,k)
            newdir = pathfy(newdir,namefy(src))
            if not check(newdir):
                os.mkdir(newdir)
                print('创建 '+ newdir + '目录')
            else:
                print('目录 '+ newdir + ' 已经存在，不再重新创建')
    else:
        print('文件存放文件夹内没有匹配多语言目录的项目')


def removecopydir(src,targ):
    langs = []
    src_list = [namefy(i) for i in scanfile(src)]
    targ_list = [namefy(i) for i in scandir(targ)]
    for i in targ_list:
        for j in src_list:
            if match_rules(j, i):
            # fnmatch(j , '*'+i+'*') or match_special(j,i):
                if i not in langs:
                    langs.append(i)
    if langs !=[]:
        for k in langs:
            newdir = pathfy(targ, k)
            newdir = pathfy(newdir, namefy(src))
            if check(newdir) and os.listdir(newdir)==[]:
                shutil.rmtree(newdir)
                print('移除 ' + newdir + '目录')
            else:
                print('地址有误或者文件夹内有内容，无法移除')
    else:
        print('文件存放文件夹内没有匹配多语言目录的项目')

# makecopydir('D:\python\测试文件夹3\【ID1234567】【平面】【美术】【CB2】CB2 社媒头图','D:\python\测试文件夹3\Community')

def getlog(log,dir):
    filelist = []
    file = open(log,'r')
    while True:
        line = file.readline()
        if line:
            filelist.append(line[:-1])
        else:
            break
    regain(filelist,dir)


def regain(list,dir):
    if os.path.exists(dir):
        for i in list:
            if os.path.exists(i):
                shutil.move(i,dir)
                print(i+'移动至'+ dir)
            else:
                continue
    else:
        print('所选路径不存在')

#下方所有代码为UI部分
class basedesk():
    def __init__(self,master):
        self.window = master
        self.window.config()
        self.window.title('文件归档')
        self.window.geometry('400x400')
        initface(self.window)

class initface():
    def __init__(self,master):
        self.master = master
        self.face = tkinter.Frame(self.master)
        self.face.pack()
        content(self.face)
        retrival(self.face)
        MakeCopy(self.face)


class content():
    def __init__(self,master):
        self.master = master
        self.face = tkinter.Frame(self.master)
        self.face.pack(fill='both')

        tkinter.Label(self.face, text='文件归档', font=('Microsoft YaHei', 13, 'bold')).grid(column=0, row=0)
        tkinter.Label(self.face,text='起点目录地址',font = ('Microsoft YaHei', 12)).grid(column=0,row=1)
        self.s1 = tkinter.Entry(self.face)
        self.s1.grid(column=1,row=1)

        tkinter.Label(self.face, text='文件放置地址', font=('Microsoft YaHei', 12)).grid(column=0, row=2)
        self.s2 = tkinter.Entry(self.face)
        self.s2.grid(column=1, row=2)

        tkinter.Button(self.face, text='开始移动',font=('Microsoft YaHei', 12),command=self.thread_it).grid(column=0, row=3)


    def thread_it(self):
        t1 = threading.Thread(target=self.callmove)
        t1.setDaemon(True)
        t1.start()

    def callmove(self):
        try:
            self.current_path = self.s1.get()
            self.source_path = self.s2.get()
            print('起点地址'+self.current_path)
            print('图片地址'+self.source_path)
            self.file_list = os.listdir(self.current_path)
            self.currentlist = [name for name in self.file_list if os.path.isdir(pathfy(self.current_path, name))]
            self.currentlist = [pathfy(self.current_path, i) for i in self.currentlist]

            self.source_list = os.listdir(self.source_path)
            self.sourcelist = [name for name in self.source_list if os.path.isfile(pathfy(self.source_path, name))]
            self.sourcelist = [pathfy(self.source_path, i) for i in self.sourcelist]

            for i in self.sourcelist:
                movepic(self.source_path, i, self.current_path, self.currentlist)
            input('移动结束')
        except:
            input('输入错误，按任意键退出')

class retrival():
    def __init__(self,master):
        self.master = master
        self.face = tkinter.Frame(self.master)
        self.face.pack(fill='both')

        tkinter.Label(self.face, text='文件撤回', font=('Microsoft YaHei', 13, 'bold')).grid(column=0, row=4)
        tkinter.Label(self.face,text='文件移动日志',font = ('Microsoft YaHei', 12)).grid(column=0,row=5)
        self.s1 = tkinter.Entry(self.face)
        self.s1.grid(column=1,row=5)

        tkinter.Label(self.face, text='取回放置地址', font=('Microsoft YaHei', 12)).grid(column=0, row=6)
        self.s2 = tkinter.Entry(self.face)
        self.s2.grid(column=1, row=6)


        tkinter.Button(self.face, text='开始取回',font=('Microsoft YaHei', 12),command=self.thread_it).grid(column=0, row=7)

        def dragged_files(files):
            msg = '\n'.join((item.decode('gbk') for item in files))
            self.s1.delete(0,'end')
            self.s1.insert('insert',msg)
        windnd.hook_dropfiles(self.face,func=dragged_files)


    def thread_it(self):
        t2 = threading.Thread(target=self.callmove)
        t2.setDaemon(True)
        t2.start()

    def callmove(self):
        try:
            getlog(self.s1.get(), self.s2.get())
        except:
            print('输入有误')

class MakeCopy():
    def __init__(self, master):
        self.master = master
        self.face = tkinter.Frame(self.master)
        self.face.pack(fill='both')

        tkinter.Label(self.face, text='创建目录', font=('Microsoft YaHei', 13, 'bold')).grid(column=0, row=8)
        tkinter.Label(self.face, text='仅社群特殊目录结构使用！', font=('Microsoft YaHei', 8)).grid(column=1, row=8)
        tkinter.Label(self.face, text='起始目录地址', font=('Microsoft YaHei', 12)).grid(column=0, row=9)
        self.s1 = tkinter.Entry(self.face)
        self.s1.grid(column=1, row=9)
        tkinter.Label(self.face, text='文件放置地址', font=('Microsoft YaHei', 12)).grid(column=0, row=10)
        self.s2 = tkinter.Entry(self.face)
        self.s2.grid(column=1, row=10)

        tkinter.Button(self.face, text='创建目录', font=('Microsoft YaHei', 12), command=self.thread_it3).grid(column=0,
                                                                                                          row=11)
        tkinter.Button(self.face, text='删除目录', font=('Microsoft YaHei', 12), command=self.thread_it4).grid(column=1,
                                                                                                          row=11)
    def thread_it3(self):
        t3 = threading.Thread(target=self.callmove3)
        t3.setDaemon(True)
        t3.start()

    def thread_it4(self):
        t4 = threading.Thread(target=self.callmove4)
        t4.setDaemon(True)
        t4.start()

    def callmove3(self):
        try:
            makecopydir(self.s2.get(),self.s1.get())
        except:
            print('输入不符合要求，此功能仅针对子目录为多语言名称的父目录')

    def callmove4(self):
        try:
            removecopydir(self.s2.get(),self.s1.get())
        except:
            print('输入不符合要求，此功能仅针对子目录为多语言名称的父目录')

if __name__ == '__main__':
    window = tkinter.Tk()
    basedesk(window)
    window.mainloop()




