#!/usr/bin/python3
#coding:utf-8
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def signal_plt():
    #生成序列参数 start, stop, step=...
    x = np.arange(0.0,100.0,0.01)
    y = 1 + np.sin(2 * np.pi * x)
    fig,ax = plt.subplots()
    ax.plot(x,y)
    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
    ax.grid()
    fig.savefig("test.png")
    plt.show()

def updata_line(hl,data):
    hl.set_xdata(np.append(hl.get_xdata(), data))
    hl.set_ydata(np.append(hl.get_ydata(), data))
    plt.draw()

# def simle_plot():



if __name__ == "__main__":
    #关闭窗口
    plt.close() 
    

     



