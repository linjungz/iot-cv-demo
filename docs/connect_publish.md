---
layout: post
title:  "车辆接入车联网并上传数据"
toc: true


---

本实验描述如何将车辆接入车联网后台. AWS IoT使用证书进行双向认证, 车辆接入前需要配置证书和策略,并将证书下载至车端.

## 1. 创建事物, 证书和策略

iot core上生成证书, 策略

### 1.1 登录 AWS IoT 控制台

- 登录到 AWS 管理控制台，然后选择服务中的IoT来打开 AWS IoT 控制台。

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/1.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/1.png)
</a>

- 请选择主页中的入门培训，点击入门。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/2.png">
![管理](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/2.png)
</a>

- 这段教程将带您注册设备，下载相关文件，请继续点击入门。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/3.png">
![注册事物](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/3.png)
</a>

- 请在“选择平台“选择“Linux/OSX”， 选择AWS IoT设备开发工具包选择“Python”，点击下一步。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/4.png">
![单个事物](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/4.png)
</a>

### 1.2 注册物品并下载证书

- 在这一步我们将开始注册物品，请为物品输入您喜欢的名称。这里为物品命名为“MyIoTDevice",请勿输入中文。点击下一步。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/5.png">
![名字](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/5.png)
</a>

- 这里为您刚刚注册的设备生成了一个策略、证书以及私有密钥。策略可以稍后查看，请点击“下载连接工具包”。工具包下载完毕后您会获得一个叫”connect_device_package.zip“的文件，请点击下一步。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/6.png">
![名字](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/6.png)
</a>

- 这一步告诉您如何配置和测试设备，我们将在启动EC2虚拟机后用到，点击“完成”。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/7.png">
![名字](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/7.png)
</a>

- 继续点击“完成”以完成IoT入门。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/8.png">
![名字](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/8.png)
</a>

- 回到IoT主页，此时在管理-物品将能看的您刚刚注册的物品。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/9.png">
![名字](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/9.png)
</a>

- 解压刚刚的”connect_device_package.zip“文件， 您会获得4个文件
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/10.png">
![名字](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/10.png)
</a>

## 2. 安装SDK并连接设备

### 2.1 安装SDK

- 将刚刚下载的 “connect_device_package”文件夹中的文件上传至您的EC2中并与您的压缩包处于同一文件夹内。运行以下命令解压：

```sh
unzip connect_device_package.zip
```

- 运行以下命令检查EC2中是否安装了git

```sh
git --version
```

- 如没有安装git，请使用以下命令安装

```sh
sudo yum install git -y
```

- 进入解压后的文件夹中，添加执行权限

```sh
chmod +x start.sh
```

- 运行启动脚本，脚本将自动下载根证书以及SDK并启动连接

```sh
sudo ./start.sh
```

- 回到IoT主页中，进入测试并点击订阅
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page2/1.png">
![订阅](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page2/1.png)
</a>

- 在订阅主题栏中输入“#”并点击订阅主题，您将看到从您的EC2发送的“Hello World!“消息。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page2/2.png">
![Hello](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page2/2.png)
</a>

## 3. 运行car_publish.py文件

###3.1 更改
