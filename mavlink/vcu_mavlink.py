import argparse
from serial import Serial
from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from mavcrc import x25crc
from struct import pack,unpack

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

def get_serial_str_cndid_payload(ser):
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

def get_serial_mavlink(ser):
    global cnt
    header = ser.read(1)
    if header == b'\xfd':
        by_len = ser.read(1)
        if len(by_len) == 1:
            d_len = unpack("<B", by_len)[0]
            syc_payload = ser.read(d_len+10)
            if len(syc_payload) == d_len+10:
                msg_id = unpack("<H", syc_payload[5:7])[0]
                paload = syc_payload[10:]
                print("msg_id:{}".format(msg_id))
                print(paload)


buf_heard = [0xfd]
buf_len = [0x0c]
hx_mavlink_sys5 = [0x00,0x01,0x02,0x03,0x04]
msgid = [0xb9,0x0b,0x00]
crc_extra = [143]
payload_canid = [0x28,0x21,0x64,0x0c]
payload_data = [0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08]

hx_mavlink_header = buf_len+hx_mavlink_sys5+msgid
hx_mavlink_paload = payload_canid+payload_data
crc_pack = x25crc()
crc_pack.accumulate(hx_mavlink_header)
crc_pack.accumulate(hx_mavlink_paload)
crc_pack.accumulate(crc_extra)
checksum = [crc_pack.crc]

mavlink_buf = buf_heard+hx_mavlink_header+hx_mavlink_paload+checksum
# mavlink_buf_pack = pack("<B")

if __name__ == "__main__":
    ser,s = serial_write_init()

    while True:
        pack_raw = b'\xfd\x0c\x00\x00*\x01\x01\xb9\x0b\x00(!d\x0c\x01\x02\x03\x04\x05\x06\x07\x08\xc5\xd4'
        ser.write(pack_raw)
        sleep(0.01)
        get_serial_mavlink(ser)

