from serial import Serial
from socket import socket, AF_INET, SOCK_DGRAM
from struct import unpack
import pickle
import argparse
import json
from binascii import b2a_hex


cnt = 0

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

def get_serial_str(ser):
    global cnt
    header = ser.read(1)
    if header == b'\xfd':
        by_len = ser.read(1)
        if len(by_len) == 1:
            d_len = unpack("<B", by_len)[0]
            syc_payload = ser.read(d_len+10)
            if len(syc_payload) == d_len+10:
                msg_id = unpack("<H", syc_payload[5:7])[0]
                # print("msg_id:{}".format(msg_id))
                if msg_id == 3002:
                    can_id = unpack("<I", syc_payload[9:13])[0]
                    print("can_id:{}".format(hex(can_id)))
                    payload = unpack("<BBBBBBBB", syc_payload[13:21])
                    print("payload:",payload)
                    cnt += 1
                    print("cnt:{}".format(cnt))
                    head_payload_data = header+by_len+syc_payload
                    print(head_payload_data)
                elif msg_id == 3001:
                    can_id = unpack("<I", syc_payload[9:13])[0]
                    print("can_id:{}".format(hex(can_id)))
                    payload = unpack("<BBBBBBBB", syc_payload[13:21])
                    print("payload:",payload)
                    cnt += 1
                    print("cnt:{}".format(cnt))
                    head_payload_data = header+by_len+syc_payload
                    print(head_payload_data)



    
if __name__ == "__main__":
    ser,s = serial_write_init()
    while True:
        get_serial_str(ser)




# if __name__ == "__main__":

#     payload_i = 0
#     ser,s = serial_write_init()
#     f = open("log.txt", "w", encoding="utf-8")
#     try:
#         while True:
#             header = ser.read(1)
#             if len(header) > 0:
#                 if header == b'\xfd':
#                     len_pack = ser.read(1)
#                     f.write(b2a_hex(len_pack).decode("ascii"))
#                     len_ = unpack("<B", len_pack)[0]
#                     i_c_s_s_c_data = ser.read(5)
#                     f.write(b2a_hex(i_c_s_s_c_data).decode("ascii"))
#                     msg_id_pack = ser.read(3)
#                     f.write(b2a_hex(msg_id_pack).decode("ascii"))
#                     msg_id = unpack("<HB", msg_id_pack)[0]
#                     can_id_pasck = ser.read(len_)
#                     f.write(b2a_hex(can_id_pasck).decode("ascii"))
#                     if msg_id == 3002:
#                         # can_id = unpack("<IBBBBBBBB", can_id_pasck)[0]
#                         payload_i += 1
#                         print("payload_i:",payload_i)
#                     # if msg_id == 3002:
#                     #     payload_i += 1
#                     # else:
#                     #     pass
#                     #     # print("loss")
#                     # payload_pack = ser.read(8)
#                     # payload = unpack("<BBBBBBBB", payload_pack)
#                     # if msg_id == 3002:
#                     #     print("  msg_id:",msg_id)
#                     #     print(" payload:",payload)
#                     #     print("payload_i:",payload_i)
#                     # else:
#                     #     pass
#                         # print("lost")
#                 else:
#                     pass
#                     # print("no header")
#     except:
#         f.close()



