---
layout: post
title:  "模拟远程进行灯光控制"
toc: true


---

## 指令下发

本实验模拟远程进行灯光控制

### 1. 通过Shadow进行控制指令下发

- 模拟app端发出温度控制指令
- 车端接受指令并进行动作
- 车端将更新后的状态重新上报到车联网平台

#### 演示代码

- light.py  模拟app端

- light_controller.py 模拟灯光控制器

在完成本实验之前，请确保您已经先后完成了"用Cloud9创建IoT设备"，"车辆接入车联网并上传数据"的实验，此时您已经启动了Cloud9，在控制台注册好了一个IoT设备，并在Cloud9上传了此设备相关的证书。

- 默认您注册了一个IoT设备，并配置好了相关策略。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/9.png">
</a>

![名字](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/9.png)

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/12.png">
</a>

![名字](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/page1/12.png)

- 默认您在Cloud9中拥有这些文件

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/code/4.png">
</a>

![Hello](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/code/4.png)

- 此时我们可以开始新的步骤了。

- 在终端中输入此命令来下载light.py文件

```sh
wget https://raw.githubusercontent.com/lanskyfan/iot-cv-demo/master/src/car_publish.py
```

- 在终端中输入此命令来下载light_controller.py文件

```sh
wget https://raw.githubusercontent.com/lanskyfan/iot-cv-demo/master/src/car_publish.py
```

- 此时您的所有文件将包括以下这些
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/1.png">
</a>

![Hello](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/1.png)

- 将light.py中的IoT终端节点、证书、私钥文件名替换为您的节点以及文件名：

```python
#Setup MQTT client and security certificates
shadowc = AWSIoTMQTTShadowClient('Light1')
mqttc.configureEndpoint("ChangeToYouEnd.iot.cn-north-1.amazonaws.com.cn",8883) # 需要更改（方法见下文）

mqttc.configureCredentials(
  './root-CA.crt',                # 参考Cloud9中的文件名更改
  './MyIoTDevice.private.key',    # 参考Cloud9中的文件名更改
  './MyIoTDevice.cert.pem'        # 参考Cloud9中的文件名更改
)
```

- 改变light.py中的Device Shadow Handler名称

```python
#Create Device Shadow Handler with persistent subscription
deviceShadowHandler = shadowc.createShadowHandlerWithName('MyIoTDevice', True) # 改为您的IoT设备名称
```

- 将light_controller.py中的IoT终端节点、证书、私钥文件名替换为您的节点以及文件名：

```python
#Setup MQTT client and security certificates
shadowc = AWSIoTMQTTShadowClient('Light1_controller')
mqttc.configureEndpoint("ChangeToYouEnd.iot.cn-north-1.amazonaws.com.cn",8883) # 需要更改（方法见下文）

mqttc.configureCredentials(
  './root-CA.crt',                # 参考Cloud9中的文件名更改
  './MyIoTDevice.private.key',    # 参考Cloud9中的文件名更改
  './MyIoTDevice.cert.pem'        # 参考Cloud9中的文件名更改
)
```

- 寻找终端节点的方式同上。

- 改变light_controller.py中的Device Shadow Handler名称

```python
#Create Device Shadow Handler with persistent subscription
deviceShadowHandler = shadowc.createShadowHandlerWithName('MyIoTDevice', True) # 改为您的IoT设备名称
```

- 在终端使用python3运行您的light.py文件,您将在终端看到如下输出，表示您已经成功初始化了设备。

```sh
python3 light.py
```

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/2.png">
</a>

![Hello](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/2.png)

- 请在终端按Enter

- 回到IoT主页中，进入您物品的影子页面，可以看到刚刚生成的影子状态以及元数据。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/3.png">
</a>

![订阅](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/3.png)

- 返回Cloud9页面，新建终端，运行您的light_controller.py

```sh
python3 light_controller.py
```

- 按照提示输入您希望更改的灯泡的颜色以及亮度

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/4.png">
</a>

![Hello](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/4.png)

- 返回运行light.py的终端，您将收到刚刚对device所做的更改，点击Enter

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/5.png">
</a>

![Hello](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/5.png)

- 在物品的影子栏目，您将看到新的影子状态

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/6.png">
</a>

![Hello](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/control/6.png)
