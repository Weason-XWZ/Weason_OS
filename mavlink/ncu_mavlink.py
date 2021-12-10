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

def get_serial_str(ser):
    header = ser.read(1)
    if header == b'\xfd':
        len = ser.read(1)
        print("len:",len)
        i_c_s_s_c_data = ser.read(5)
        # print("i_c_s_s_c_data:",i_c_s_s_c_data)
        msg_id_pack = ser.read(3)
        msg_id = unpack("<HB", msg_id_pack)[0]
        print("msg_id:",msg_id)
        can_id_pasck = ser.read(4)
        can_id = unpack("<I", can_id_pasck)[0]
        print("can_id:",hex(can_id))
        payload_pack = ser.read(8)
        payload = unpack("<BBBBBBBB", payload_pack)
        print("payload:",payload)




if __name__ == "__main__":

    ser,s = serial_write_init()
    print("mavlink python Qt")
    while True:
        get_serial_str(ser)

