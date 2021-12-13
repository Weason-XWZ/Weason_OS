from serial import Serial
from struct import unpack

s = Serial("COM16", 460800, timeout=3)


cnt = 0
while True:
    d = s.read(1)
    if d == b'\xfd':
        d_len = s.read(1)
        if len(d_len) == 1:
            d_len = unpack("<B", d_len)[0]
            # print(d_len)
            data = s.read(d_len+10)
            if len(data) == d_len+10:
                id = unpack("<H", data[5:7])[0]
                # print(id)
                if id == 3002:
                    cnt += 1
                    print("cnt:{}".format(cnt))
