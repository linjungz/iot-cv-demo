# 基于AWS IoT动手搭建一个车联网平台
基于AWS IoT构建车联网平台的演示环境，并作为IoT Builder's Day的动手实验材料

## 目标
- 通过AWS IoT服务构建一个完整的车联网平台, 包括车辆接入与管理, 数据上传与指令下发, OTA等车联网常见功能.
- 整个演示环境可以完全运行在AWS国内区域
- 操作文档与界面截图均为中文

## 内容框架
### AWS IoT 基本功能

#### [Lab 00. 实验环境准备](docs/00_cloud9.md)
在这个实验中我们将会演示如何在AWS中国区域Marketplace启动一台带有Cloud9 Web IDE的EC2实例，后续实验会以此实例运行相应的python脚本，以模拟IoT设备行为。

#### [Lab 01. IoT接入与消息发送](docs/01_connect_publish.md)
在这个实验中我们将演示如何创建一个IoT Thing并将模拟设备接入AWS IoT，通过模拟设备向AWS IoT云端发送传感器数据

#### [Lab 02. 设备状态控制](docs/02_control.md)
在这个实验中我们将演示如何利用AWS IoT Shadow来进行设备状态的控制

#### [Lab 03. 数据在云端展现](docs/02_data_visualize.md)
在这个实验中我们将演示如何将AWS IoT云端收集到的传感器数据通过Rule Engine保存至ElasticSearch中，并利用Kibana进行实时展现

#### 实验内容持续更新中...
