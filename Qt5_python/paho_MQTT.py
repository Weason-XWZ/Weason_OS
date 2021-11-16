import paho.mqtt.client as mqtt
import time
import datetime

# 定义回调
def on_connect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def on_publish(msg, rc):   # 成功发布消息的操作
    if rc == 0:
        print("publish success, msg = " + msg)
 
def on_connect(client, userdata, flags, rc):   # 连接后的操作 0为成功
    print("Connection returned " + str(rc))


if __name__ == "__main__":
# 服务端
   client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
   client =  mqtt.Client(client_id)
   client.username_pw_set("用户名","密码")
   client.on_connect = on_connect
   client.on_message = on_message
   client.connect("连接地址", 1883, 60)
   client.loop_forever()

# # 客户端

# client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
# client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
# client.username_pw_set("用户名", "密码")  # 设置用户名，密码
# client.connect("链接地址", "1833", 60)  # 连接服务 keepalive=60
# client.on_connect = on_connect  # 连接后的操作
# client.loop_start()
# time.sleep(2)
# count = 0
 
# while count < 5:  # 发布五条消息
#     count = count + 1
#     msg = str(datetime.datetime.now())
#     rc, mid = client.publish("发布消息的主题", payload=msg, qos=1)  # qos
#     on_publish(msg, rc)



