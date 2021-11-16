#!/usr/bin/python3
#coding:utf-8

import argparse
from serial import Serial
from time import time, sleep
from math import sin,cos, pi
from struct import calcsize, pack

header = b'\xaa'
tailer = b'\x55'

parser = argparse.ArgumentParser(description="sender")
parser.add_argument('-p','--port',help="set serial port")
parser.add_argument('-b','--baudrate', help="set  serial port baudrate", type=int)
args = parser.parse_args()
print(args.port)  
print(args.baudrate)

ser = Serial(args.port, baudrate=args.baudrate)

while True:
    timestamp = time()
    x = sin(timestamp)
    y = cos(timestamp)
    z = (timestamp/(2*pi) - int(timestamp/(2*pi)))*2*pi
    id = 0
    payload = pack("<fff", x, y,z)
    id_raw = pack("<H", id)
    payload_len_raw = pack("<H", len(payload))
    pack_raw = header+id_raw+payload_len_raw+payload+tailer
    ser.write(pack_raw)
    sleep(0.01)
    # id_raw = pack("<H", 1)
    # payload_len_raw = pack("<H", calcsize("<dff"))
    # payload = pack("<dff", timestamp,x,y)
    # pack_raw = header+id_raw+payload_len_raw+payload+tailer
    # ser.write(pack_raw)
    # sleep(0.01)