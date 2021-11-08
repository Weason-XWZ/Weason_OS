from serial import Serial
from socket import socket, AF_INET, SOCK_DGRAM
from struct import unpack
import pickle
import argparse

def serial_write_init():
    parser = argparse.ArgumentParser(description="serial2json program")
    parser.add_argument("-p", "--port", help="set serial port")
    parser.add_argument("-b", "--baudrate", help="set serial baudrate")
    args = parser.parse_args()
    # "127.0.0.1"
    #  回送地址：127.0.0.1。一般用于测试使用。例如：ping 127.0.0.1 来测试本机TCP/IP是否正常。
    # 
    s = socket(AF_INET, SOCK_DGRAM)
    ser = Serial(args.port, baudrate=args.baudrate, timeout=3)
    return ser,s

# def hx_mav_crc_init():
#     return 0xffff

def hx_mav_crc_accumulate(crc:hex,data:hex):
    tmp = data^crc
    tmp ^= (tmp<<4)
    crc = (crc>>8)^(tmp<<8)^(tmp<<3)^(tmp>>4)
    return crc

def checksum_crc(checksum:hex,crc:hex):
    if checksum == crc:
        return 0
    else:
        return 1

def get_serial_str(ser):
    header = ser.read(1)
    if header == b'\xaa':
        id_raw = ser.read(2)
        if len(id_raw) != 2:
            return 
        payload_len_raw = ser.read(2)
        if len(payload_len_raw) != 2:
            return 
        payload_len = unpack("<H", payload_len_raw)[0]
        crc = 0xffff
        print(type(crc))
        print(type(payload_len))



if __name__ == "__main__":

    ser,s = serial_write_init()
    print("mavlink python Qt")
    while True:
        get_serial_str(ser)

