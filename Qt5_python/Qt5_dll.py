from ctypes import *
import time

dll = windll.LoadLibrary("D:/Program Files/Ecantools/drv/CHUSBDLL64.dll")
print(dll)
rst = dll.OpenDeviceFD(4,0,0)






