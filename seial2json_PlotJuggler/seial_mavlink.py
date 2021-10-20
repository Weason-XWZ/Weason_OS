from serial import Serial
from socket import socket, AF_INET, SOCK_DGRAM

def serial_write_init(port,baudrate):
    # "127.0.0.1"
    #  回送地址：127.0.0.1。一般用于测试使用。例如：ping 127.0.0.1 来测试本机TCP/IP是否正常。
    # s = socket(AF_INET, SOCK_DGRAM)  底层网络协议
    s = socket(AF_INET, SOCK_DGRAM) 
    ser = Serial(port, baudrate=baudrate, timeout=3)
    return ser,s

def get_serial_str(ser,s):
    header = ser.read(1)
    if header == b'\xfd':
        buf_len = ser.read(1)

if __name__ == "__main__":

    ser,s = serial_write_init("COM11",115200)

    while True:
        get_serial_str(ser,s)

