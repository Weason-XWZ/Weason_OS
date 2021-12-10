import paho.mqtt.client as mqtt
import hmac,time


# {
#   "ProductKey": "gkt3LDoidbE",
#   "DeviceName": "PcgetHot",
#   "DeviceSecret": "e53c52e954a87bcf10efd26bcf20bfeb"
# }

ProductKey = 'gkt3LDoidbE'
DeviceName = 'PcgetHot'
DeviceSecret = "e53c52e954a87bcf10efd26bcf20bfeb"

# topic (iot后台获取)
POST = '/sys/gkt3LDoidbE/pi4bMqtt/thing/event/property/post'  # 上报消息到云
POST_REPLY = '/sys/gkt3LDoidbE/pi4bMqtt/thing/event/property/post_reply'  
SET = '/sys/gkt3LDoidbE/pi4bMqtt/thing/service/property/set'  # 订阅云端指令

def linkiot(DeviceName,ProductKey,DeviceSecret,server = 'iot-as-mqtt.cn-shanghai.aliyuncs.com'):
    serverUrl = server
    ClientIdSuffix = "|securemode=3,signmethod=hmacsha256,timestamp="

    # 拼合
    Times = str(int(time.time()))  # 获取登录时间戳
    Server = ProductKey+'.'+serverUrl    # 服务器地址
    ClientId = DeviceName + ClientIdSuffix + Times +'|'  # ClientId
    userNmae = DeviceName + "&" + ProductKey
    PasswdClear = "clientId" + DeviceName + "deviceName" + DeviceName +"productKey"+ProductKey + "timestamp" + Times  # 明文密码

    # 加密
    h = hmac.new(bytes(DeviceSecret,encoding= 'UTF-8'),digestmod=hashlib.sha256)  # 使用密钥
    h.update(bytes(PasswdClear,encoding = 'UTF-8'))
    Passwd = h.hexdigest()
    return Server,ClientId,userNmae,Passwd

# 消息回调（云端下发消息的回调函数）
def on_message(client, userdata, msg):
    print(msg.payload)
    Msg = json.loads(msg.payload)
    data = Msg['params']['car_state']    


#连接回调（与阿里云建立链接后的回调函数）
def on_connect(client, userdata, flags, rc):
    pass

if __name__ == "__main__":
    Server,ClientId,userNmae,Password = linkiot(DeviceName,ProductKey,DeviceSecret)
    ali_mqtt = mqtt.Mqtt(Server,ClientId,userNmae,Password)
    mqtt.subscribe(SET) # 订阅服务器下发消息topic
