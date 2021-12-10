#!/usr/bin/python3

from http import server
import aliLink,mqttd,rpi
import time,json
import argparse

state_car = 0

def get_state_car():
    global state_car
    return state_car

def set_state_car(data):
    global state_car
    state_car = data



# 三元素（iot后台获取）
ProductKey = 'gkt3LDoidbE'
DeviceName = 'PcgetHot'
DeviceSecret = "e53c52e954a87bcf10efd26bcf20bfeb"
# topic (iot后台获取)
POST = '/sys/gkt3LDoidbE/PcgetHot/thing/event/property/post'  # 上报消息到云
POST_REPLY = '/sys/gkt3LDoidbE/PcgetHot/thing/event/property/post_reply'  
SET = '/sys/gkt3LDoidbE/PcgetHot/thing/service/property/set'  # 订阅云端指令


# 消息回调（云端下发消息的回调函数）
def on_message(client, userdata, msg):
    print(msg.payload)
    Msg = json.loads(msg.payload)
    data = Msg['params']['car_state']
    set_state_car(data)
    


#连接回调（与阿里云建立链接后的回调函数）
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/#")

# 链接信息
Server,ClientId,userNmae,Password = aliLink.linkiot(DeviceName,ProductKey,DeviceSecret)
# mqtt链接
mqtt = mqttd.MQTT(Server,ClientId,userNmae,Password)
mqtt.subscribe(SET) # 订阅服务器下发消息topic
mqtt.begin(on_message,on_connect)


# 信息获取上报，每10秒钟上报一次系统参数
while True:
    time.sleep(2)

    # CPU 信息
    # CPU_temp = float(rpi.getCPUtemperature())  # 温度   ℃
    # CPU_usage = float(rpi.getCPUuse())         # 占用率 %

    CPU_temp = 40
    CPU_usage = 50
 
    # RAM 信息
    # RAM_stats =rpi.getRAMinfo()
    # RAM_total =round(int(RAM_stats[0]) /1000,1)    # 
    # RAM_used =round(int(RAM_stats[1]) /1000,1)
    # RAM_free =round(int(RAM_stats[2]) /1000,1)

    RAM_stats = 100
    RAM_total = 60
    RAM_used = 30
    RAM_free = 50
 
    # Disk 信息yt
    # DISK_stats =rpi.getDiskSpace()
    # DISK_total = float(DISK_stats[0][:-1])
    # DISK_used = float(DISK_stats[1][:-1])
    # DISK_perc = float(DISK_stats[3][:-1])

    DISK_stats = 20
    DISK_total = 30
    DISK_used = 40
    DISK_perc = 50

    #汽车启动状态
    state_car = get_state_car()
    # 构建与云端模型一致的消息结构
    updateMsn = {
        'cpu_temperature':CPU_temp,
        'cpu_usage':CPU_usage,
        'RAM_total':RAM_total,
        'RAM_used':RAM_used,
        'RAM_free':RAM_free,
        'DISK_total':DISK_total,
        'DISK_used_space':DISK_used,
        'DISK_used_percentage':DISK_perc,
        'car_state':state_car
    }
    JsonUpdataMsn = aliLink.Alink(updateMsn)
    print(JsonUpdataMsn)

    mqtt.push(POST,JsonUpdataMsn) # 定时向阿里云IOT推送我们构建好的Alink协议数据
