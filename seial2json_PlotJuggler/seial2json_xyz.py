#!/usr/bin/python3
# coding:utf-8

from ast import With
from binascii import b2a_hex
from struct import pack, unpack, calcsize
import json
from serial import Serial
import argparse
from socket import socket, AF_INET, SOCK_DGRAM
import csv


def serial_write_init(port,baudrate):
    # parser = argparse.ArgumentParser(description="serial2json program")
    # parser.add_argument("-p", "--port", help="set serial port")
    # parser.add_argument("-b", "--baudrate", help="set serial baudrate")
    # args = parser.parse_args()
    # "127.0.0.1"
    #  回送地址：127.0.0.1。一般用于测试使用。例如：ping 127.0.0.1 来测试本机TCP/IP是否正常。
    # s = socket(AF_INET, SOCK_DGRAM)  底层网络协议
    s = socket(AF_INET, SOCK_DGRAM) 
    ser = Serial(port, baudrate=baudrate, timeout=3)
    return ser,s

# shell 参数初始化
def serial_shellinit():
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


# |header(0xaa) | id(u16) | payload len(u16) | payload | tailer(0x55) |
def get_serial(ser,s,ip_addr,desc):
    header = ser.read(1)
    if header == b'\xaa':
        id_raw = ser.read(2)
        if len(id_raw) != 2:
            return 
        payload_len_raw = ser.read(2)
        if len(payload_len_raw) != 2:
            return 
        payload_len = unpack("<H", payload_len_raw)[0]
        payload_raw = ser.read(payload_len)
        if len(payload_raw) != payload_len:
            return 
        tailer = ser.read(1)
        if tailer != b'\x55':
            return 
        id = unpack("<H", id_raw)[0]
        members_desc = [{"name": x["name"], "pack_format":x["pack_format"],
                            "members":x["members"]} for x in desc["msgs"] if x["id"] == id]
        if len(members_desc) < 1:
            return 
        member_desc = members_desc[0]
        keys = member_desc["members"].keys()
        if calcsize(member_desc["pack_format"]) == payload_len:
            data = unpack(member_desc["pack_format"], payload_raw)
            # print(data[0])
            # print(data[1])
            # print(data[2])
            data_json = {member_desc["name"]: dict(zip(keys, data))}
            fcsvs[member_desc["name"]].write((",".join(['{}']*len(data))+'\n').format(*data))
            str_json = json.dumps(data_json)
            print(str_json)
            s.sendto(str_json.encode("utf-8"), ip_addr)


# 取JSON文件的结构体框架
def get_json():
    f = open("packet_descript.json", "r")
    desc = json.load(f)
    f.close()
    data = desc["msgs"][0]["members"]
    print(data)
    return f,desc

#输出CVS文件
def get_csv():
    names = [i["name"] for i in desc["msgs"]]
    csvs = [open(i["name"]+'.csv', "w",encoding="utf-8") for i in desc["msgs"]]
    fcsvs = dict(zip(names,csvs))
    return fcsvs


if __name__ == "__main__":
    
    ser,s = serial_shellinit()
    # ser,s = serial_write_init("COM11",115200)
    ip_addr = ("127.0.0.1", 9870)
    f,desc = get_json()

    fcsvs = get_csv()

    for i in desc["msgs"]:
        mkeys = i["members"].keys()
        sformat = (",".join(['{}']*len(mkeys))) + '\n'
        fcsvs[i["name"]].write(sformat.format(*mkeys))


    try:
        while True:
            get_serial(ser,s,ip_addr,desc)
    except:
        print('\n')
        for k in fcsvs.items():
            k[1].close()
            print("close file {}.csv".format(k[0]))
    
