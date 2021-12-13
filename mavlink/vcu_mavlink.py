import argparse
from serial import Serial
from time import time, sleep
from math import sin,cos, pi
from struct import calcsize, pack

header = 0xfd
led = 0x08
i_c_s_s_c_data = b'\x00\x00\xa5\x01\x01'
#msg_id = 3001
msg_id = 3001 
#
can_id = 0x0C642128 
payload = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08]

parser = argparse.ArgumentParser(description="sender")
parser.add_argument('-p','--port',help="set serial port")
parser.add_argument('-b','--baudrate', help="set  serial port baudrate", type=int)
args = parser.parse_args()
print(args.port)  
print(args.baudrate)

ser = Serial(args.port, baudrate=args.baudrate)

while True:

    header_pack = pack("<H",header)
    len_pack = pack("<H",len)
    i_c_s_s_c_data_pack = pack("<HHHHH",i_c_s_s_c_data)
    msg_id_pack = pack("<HHH",msg_id)
    can_id_pasck = pack("<HHHH",can_id)
    payload_pack = pack("<HHHHHHHH",payload)
    crc_pack = pack("")
    pack_raw = header_pack+len_pack+i_c_s_s_c_data_pack+msg_id_pack+can_id_pasck+payload_pack+crc_pack
    ser.write(pack_raw)
    sleep(0.01)

