---
layout: post
title:  "数据存储与展现"
toc: true


---

通过IoT Core Rule Egine连接其他aws服务.本实验将数据存入ElasticSearch并通过Kibana进行展现

## 1. 部署ElasticSearch

### 1.1 通过ElasticSearch建立ES域

- 在AWS官网通过搜索进入Elasticsearch Service。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/1.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/1.png)
</a>

- 在Elasticsearch Service首页选择“创建新域”。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/2.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/2.png)
</a>

- 选择部署类型为“开发和测试”，Elasticsearch 选择版本为“6.7”，点击下一步。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/3.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/3.png)
</a>

- 配置Elasticsearch域名为“iot-lab”， 实例类型选择“r5.large.elasticsearch“，实例数量选择为1。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/4.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/4.png)
</a>

- 其余配置如果与图片中相同，则无需更改，检查完毕后直接点击下一步。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/5.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/5.png)
</a>
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/6.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/6.png)
</a>

- 网络配置选择“公有访问权限”， 访问策略选择允许从特定IP访问域，一个窗口会弹出，您需要在窗口输入您的公有IP或者对应的CIDR形式，公网IP可通过这个网站获取: [What Is My IP](https://www.whatismyip.com/)
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/6a.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/6a.png)
</a>

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/7.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/7.png)
</a>

- 此时您的访问策略应该显示为如下形式, "aws:SourceIp":之后是您的IP地址，确认之后点击下一步。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "es:*",
      "Resource": "arn:aws-cn:es:cn-north-1:XXXXXXXXXXXX:domain/iot-lab/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "XXXXXXXXXXXX"
        }
      }
    }
  ]
}
```

- 检查之前的配置，点击确认，您将在控制面看见您的新域。稍等十分钟之后，您的域状态将变成绿色的有效。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/8.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/8.png)
</a>

- 在此处您将看到Kibana链接，点击Kibana链接以访问Kibana网页，如果无法进入网页，请再次检查您的IP地址是否正确，如果有问题请修改访问策略。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/9.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/9.png)
</a>
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/10.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/10.png)
</a>

### 1.2 在Elasticsearch集群上建立索引

- 索引建立
- 访问权限介绍

- 在这里我们使用HTTP请求来建立索引，请在终端输入如下命令，请把最下面一行的链接替换为您的集群的终端节点，在控制面板可以找到

```sh
curl -H 'Content-Type: application/json' -i -X PUT -d '{
  "mappings": {
    "truck": {
      "properties": {
        "timestamp": {
          "type": "long",
          "copy_to": "datetime"
        },
        "datetime": {
          "type": "date",
          "store": true
        },
        "location": {
          "type": "geo_point"
        },
        "battery":{
        "type": "float"
        },
        "engine_temperature":{
        "type": "short"
        },
        "pressure":{
        "type": "short"
        },
        "rpm":{
        "type": "short"
        },
        "cargo_temperature":{
        "type": "short"
        }
      }
    }
  }
}
' 'https://search-iot-lab-xxxxxxxxxxxxxxxxxxxxx.cn-north-1.es.amazonaws.com.cn/trucks'
```

如果成功您将收到状态“ {“acknowledged”:true)”。如果无法访问，请检查Kibana能否进入。如果不能进入，请调整访问策略。

## 2. 设置规则将数据存入ES

- IoT Core Rule Engine设置

### 2.1 创建IAM角色

- 打开AWS IAM服务，选择侧边栏的角色，点击创建角色
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/20.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/20.png)
</a>

- 在AWS产品中选择IoT，点击下一步：权限
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/21.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/21.png)
</a>

- 点击下一步：标签
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/22.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/22.png)
</a>

- 点击下一步：审核
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/23.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/23.png)
</a>

- 添加角色名称为：“iot-es-action-role“，点击创建角色
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/24.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/24.png)
</a>

### 2.2 创建IoT规则

- 进入IoT服务，进打开侧边栏的行动，点击右上角的创建
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/25.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/25.png)
</a>

- 添加规则名称为ElasticsearchLab
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/26.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/26.png)
</a>

- 在规则查询语句中输入

```SQL
SELECT *, timestamp() as timestamp FROM 'truck/#'
```

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/27.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/27.png)
</a>

- 点击添加操作，选择将消息发送到Amazon Elasticsearch Service，点击配置操作
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/28.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/28.png)
</a>

- 选择资源为"iot-lab", ID输入“${newuuid()}”，索引输入“trucks“， 类型输入“truck”。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/29.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/29.png)
</a>

- 选择角色为iot-es-action-role。 
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/30.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/30.png)
</a>

- 创建规则。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/31.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/31.png)
</a>

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/32.png">
![Get started](https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/dashboard/32.png)
</a>

### 3. 设置Kibana进行数据可视化

- Kibana Dashboard创建

