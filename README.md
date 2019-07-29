# iot-cv-demo
基于AWS IoT构建车联网平台的演示环境

## 目标
- 通过AWS IoT服务构建一个完整的车联网平台, 包括车辆接入与管理, 数据上传与指令下发, OTA等车联网常见功能.
- 整个演示环境可以完全运行在AWS国内区域
- 操作文档与界面截图均为中文

## 内容框架(待定)
### AWS IoT 基本功能
#### 车辆接入IoT并上传数据
- IoT 事物/证书/策略的创建
- MQTT Publish/Subscribe

#### 数据在云端展现
- IoT Rule Engine -> ElasticSearch -> Kibana

#### 数据在云端归档保存
- IoT Rule Engine -> Kinesis Firehose -> S3

#### 控制指令下发至车端
- IoT Shadow

#### Web端接入
- 数据展现
- 指令下发

#### OTA
- Job / Job Agent

### AWS IoT 进阶功能
#### 车辆批量接入车联网
- IoT Device Management: Bulk Provisiong

#### 车辆即时注册至车联网
- IoT JITP/JITR

#### 精细化控制车辆接入权限
- IoT Policy

#### Web端接入授权
- Cognito Identity Pool 与第三方授权结合(Amazon Login/WeChat)

### CVRA
介绍AWS车联网参考架构CVRA
