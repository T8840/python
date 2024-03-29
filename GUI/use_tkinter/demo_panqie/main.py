# -*- coding:utf-8 -*-
import tkinter as tk
import tkinter.messagebox
from winsound import Beep
import threading
import sys
import pygame
import time

# 用于统计完成的番茄钟个数
count = 0
# 线程切换标志
thread_flag = True
# 音乐开关标志
music_flag = True

# 调用Tk()创建主窗口
root = tk.Tk()
# 给主窗口起一个名字，也就是窗口的名字
root.title('Rio的番茄钟')
# 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"
root.geometry('460x300')
root.configure(bg='Tomato')


# 创建完成计时后的弹窗
def mymsg():
    try:
        tk.messagebox.showinfo("提示", "恭喜完成一个番茄钟！！记得休息一下")
    except Exception as e:
        print(type(e), e)
        sys.exit()

# 休息结束弹窗
def mymsg2():
    tk.messagebox.showinfo("提示", "休息完毕！")

# 创建番茄计时函数
# strptime()函数将字符串转换为datetime
def tomato_clock(remain_time):
    # 如果在休息时间未结束就开启番茄钟，则停止音乐
    pygame.mixer.music.pause()
    # 避免未进行番茄钟时长选择
    if remain_time == 0:
        lb3.configure(text='请先选择番茄钟时长')
        return
    print(remain_time)
    begin_time = time.strftime('%M:%S', time.gmtime(remain_time))
    lb2.configure(text=begin_time)
    lb3.configure(text='总时间/剩余时间')
    global thread_flag
    if thread_flag:
        thread_flag = False
    else:
        thread_flag = True
    tmp_thread_flag = thread_flag
    for i in range(remain_time):
        if tmp_thread_flag != thread_flag:
            return
        remain_time -= 1
        remain_time_str = time.strftime('/ %M:%S', time.gmtime(remain_time))
        lb1.configure(text=remain_time_str)
        root.update()
        time.sleep(1)
        if remain_time == 0:
            Beep(500, 800)
            tomato_count()
            mymsg()
    lb1.configure(text=begin_time)
    relax()


# 创建番茄计数的函数
def tomato_count():
    global count
    count += 1
    lb4.configure(text=count)

# 创建休息时间函数
def relax():
    remain_time = 480   # 休息8分钟
    begin_time = time.strftime('%M:%S', time.gmtime(remain_time))
    lb2.configure(text=begin_time)
    lb3.configure(text='总时间/剩余时间')

    # 线程标志，用于结束旧线程
    global thread_flag
    if thread_flag:
        thread_flag = False
    else:
        thread_flag = True
    tmp_thread_flag = thread_flag
    pygame.mixer.music.play(-1)
    for i in range(remain_time):
        if tmp_thread_flag != thread_flag:
            return
        remain_time -= 1
        remain_time_str = time.strftime('/ %M:%S', time.gmtime(remain_time))
        lb1.configure(text=remain_time_str)
        root.update()
        time.sleep(1)
        if remain_time == 0:
            pygame.mixer.music.pause()
            mymsg2()
    lb1.configure(text=begin_time)

# 音乐控制函数
def music_allow():
    global music_flag
    # 如果已经是True(即不禁止音乐时)，勾选了按钮，则music_flag 变为 False，禁止音乐
    if music_flag:
        music_flag = False
        pygame.mixer.music.set_volume(0.0)
    else:
        music_flag = True
        pygame.mixer.music.set_volume(0.5)

def resource_path(relative_path):
    if getattr(sys,'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

music_path = resource_path(os.path.join("music","music.mp3"))

if __name__ == "__main__":

    #音乐初始化
    pygame.mixer.init()
    # 异常抛出，防止没有放音乐文件
    try:
        # pygame.mixer.music.load('music.mp3')
        # pygame.mixer.music.load(music_path)
        pygame.mixer.music.load(resource_path('music/music.mp3'))

    except Exception as e:
        print(type(e), e)
        tk.messagebox.showinfo("提示", "无文件music.mp3或改文件路径不对")
        sys.exit()
    pygame.mixer.music.set_volume(0.5)
    # 创建变量
    var = tk.IntVar()
    # 给变量赋初值为30
    var.set(30)

    # 番茄动态计时
    lb1 = tk.Label(root, text='0', bg='Tomato', fg='white', font='Verdana 16 bold', width=7, height=1)
    lb1.place(x=130, y=100)

    # 番茄固定时间
    lb2 = tk.Label(root, text='0', bg='Tomato', fg='white', font='Verdana 16 bold', width=5, height=1)
    lb2.place(x=60, y=100)

    # 剩余时间/总时间
    lb3 = tk.Label(root, text=' ', bg='Tomato', fg='white', font='Verdana 16 bold', width=14, height=2)
    lb3.place(x=50, y=44)

    # 番茄个数显示
    lb4 = tk.Label(root, text='0', bg='Tomato', fg='white', font='Verdana 16 bold', width=7, height=1)
    lb4.place(x=90, y=20)

    # 左上角的 番茄：
    lb5 = tk.Label(root, text='已积累番茄：', bg='Tomato', fg='white', font='Verdana 16 bold', width=8, height=1)
    lb5.place(x=5, y=20)

    # 按钮
    ##创造一个frame来收纳按钮
    fr1 = tk.LabelFrame(root,bg='LightGreen',text='选择番茄钟时长', relief='groove', bd=1,)
    fr1.pack(side='right')
    r1 = tk.Radiobutton(fr1, text='30min', variable=var, bg='LightGreen', value=1800)
    r1.pack()
    r2 = tk.Radiobutton(fr1, text='45min', variable=var, bg='LightGreen', value=2700)
    r2.pack()
    r3 = tk.Radiobutton(fr1, text='60min', variable=var, bg='LightGreen', value=3599)
    r3.pack()
    Checkbutton = tk.Checkbutton(fr1, text="是否禁止音乐", fg='black', bg='LightGreen', command=music_allow)
    Checkbutton.pack()

    # 开启一个番茄
    #利用多线程，避免进入番茄钟后，退出按钮失效
    Button1 = tk.Button(root, text='开启一个番茄', bg='orange', fg='black', font='Verdana 13 bold',width=15,
                      height=1, command=lambda: threading.Thread(target=tomato_clock, daemon=True,args=(var.get(),)).start())
    Button1.place(x=70, y=150)

    # 休息一下
    Button2 = tk.Button(root, text='休息一下', bg='cornflowerblue', fg='black', font='Verdana 13 bold',
                        width=15, height=1, command=lambda: threading.Thread(target=relax, daemon=True).start())
    Button2.place(x=70, y=200)

    # 添加按钮，以及按钮的文本，并通过command 参数设置关闭窗口的功能
    button = tk.Button(root, text="退出", fg='black', bg='YellowGreen', width=15, command=root.quit)
    # 将按钮放置在主窗口内
    button.place(x=105, y=250)

    #开启主循环，让窗口处于显示状态
    root.mainloop()
