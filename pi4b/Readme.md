# 树莓派4b调试记录

## 账号密码

pi:123qwe

rood:123qwe

## cmd命令

#### 更新软件版本以及版本列表

`sudo apt update`

#### 更新系统版本

`sudo apt upgrade`

#### 解压到 `Downloade`文件夹

`unzip code.zip -d Downloade`

#### 压缩到 `Downloade`文件夹

`zip -r code.zip Downloade `

#### 安装gitkraken

在运行最新版本Raspbian snap的[Raspberry Pi](https://www.raspberrypi.org/)上，可以直接从命令行安装：

`sudo apt update `

`sudo apt install snapd`

您还需要重新启动设备：

`sudo reboot`

在此之后，安装 core snap 以获得最新的 snapd:

`sudo snap install core`

要安装 GitKraken，只需使用以下命令：

`sudo snap install gitkraken --classic`

![](image/Readme/1637314500111.png)

#### 接入usb查询

`lsusb`

![](image/Readme/1639655054325.png)

#### 配置界面

`sudo raspi-config`

![](image/Readme/1639660527355.png)

#### USB摄像头接入

1.查看接入的端口

![](image/Readme/1639655054325.png)

2.查看设备的端口

![](image/Readme/1639656093558.png)

3.使用 `fswebcam`命令抓图片

`sudo apt-get install fswebcam`

`fswebcam /dev/video0 ~/image.jpg`

`fswebcam --no-banner -r 640x480 image3.jpg`

4.使用视频

#### 授权编辑文件

sudo chmod 777 文件夹名字

`sudo chmod 777 motion.conf `
