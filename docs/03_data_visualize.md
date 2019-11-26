## Lab 02. 数据实时展现

在这个实验中我们将演示如何将AWS IoT云端收集到的传感器数据通过Rule Engine保存至ElasticSearch中，并利用Kibana进行实时展现

### 1. 部署ElasticSearch

- 进入ElasticSearch服务的控制台并创建一个ES域

![](./md_image/dashboard/1.jpg)
![](./md_image/dashboard/2.jpg)

- 选择部署类型为“开发和测试”，Elasticsearch 选择版本为“6.8”，点击下一步。
![](./md_image/dashboard/3.jpg)

- 配置Elasticsearch域名, 如本示例中的“es-iot-demo”， 实例类型根据处理能力需求进行选择，如本示例中的“m4.large.elasticsearch“，实例数量选择为1，其他可使用默认配置。
![](./md_image/dashboard/4.jpg)

- 网络配置选择“公有访问权限”， 为方便测试访问策略选择”允许对域进行公开访问“

![](./md_image/dashboard/5.jpg)

*注意：仅在测试环境使用该策略，在生产环境建议对权限进行更为严格的设置“

- 检查之前的配置，点击确认，您将在控制面看见您的新域。稍等十分钟之后，ES域状态变有”有效“。

![](./md_image/dashboard/6.jpg)




### 2. 通过Kibana创建索引

- 在Kibana提供的Dev Tools中，我们可以运行命令来创建索引：

![](./md_image/dashboard/7.jpg)

*通过命令 DELETE index_name 可以删除已有的索引*

在ES控制台可以看到相应的索引已经创建出来

![](./md_image/dashboard/8.jpg)


### 3. 配置AWS IoT Rule将数据导入ES

#### 3.1 创建IAM角色

需要为AWS IoT配置相应的IAM角色，以便该服务有权限可以对其他AWS服务进行操作，包括这里使用的ES

- 打开AWS IAM服务，选择侧边栏的角色，点击创建角色

![](./md_image/dashboard/20.png)

- 在AWS产品中选择IoT，点击下一步：权限

![](./md_image/dashboard/21.png)

- 点击下一步：标签

![](./md_image/dashboard/22.png)

- 点击下一步：审核

![](./md_image/dashboard/23.png)

- 添加角色名称为：“iot-es-action-role“，点击创建角色

![](./md_image/dashboard/24.png)

#### 3.2 创建IoT规则

接下来我们在IoT Rule Engine中创建规则，将数据导入至ES中

- 进入IoT服务，进打开侧边栏的”行动“，点击"创建"

![](./md_image/dashboard/50.jpg)

- 配置规则的基本信息

![](./md_image/dashboard/53.jpg)

通过规则查询语句（以SQL语法），我们可以提取指定MQTT主题下的数据，并可进行简单的预处理。相应的SQL语句如下

```SQL
SELECT *, timestamp() as timestamp FROM 'connectedcar/#'
```

- 配置规则的操作
点击添加操作，选择将消息发送到Amazon Elasticsearch Service，点击”添加操作“
![](./md_image/dashboard/55.jpg)

选择将消息发送至ES：
![](./md_image/dashboard/51.jpg)

配置相关的细节：
![](./md_image/dashboard/52.jpg)

其中角色是上一步创建的IAM角色
完成后可以看到相应操作已经添加到规则中：
![](./md_image/dashboard/54.jpg)

点击”创建规则“即可。
规则创建即生效，如果需要暂停相应的规则，可以通过控制台进行操作


### 3. 通过Kibana进行数据展示配置

#### 3.1 创建Index Pattern

- 进入Kibana的discover侧边栏，选择Create index pattern，并在index pattern中输入“cars”。匹配成功后会显示Success，之后请点击Next step
![](./md_image/dashboard/40.png)

- 从下拉菜单中选择Time Filter field name为datetime。点击create index pattern。
![](./md_image/dashboard/41.png)

- 检查刚刚创建的index pattern: cars。
![](./md_image/dashboard/42.png)

#### 3.2 打开模拟设备，检查数据是否进入ES

- 在Cloud9中运行car_publish.py，可以看到数据已经不断产生
![](./md_image/dashboard/60.jpg)

- 在Kibana中检查数据是否已经进入ES
![](./md_image/dashboard/61.jpg)


#### 3.3 进行图表设置

- 在Kibana中进入Visualize侧边栏，选择create a visualization。
![](./md_image/dashboard/43.png)

- 选择Line作为我们要创建的图的类型
![](./md_image/dashboard/44.png)

- 选择cars*
![](./md_image/dashboard/45.png)

- 打开Metrics Y-Axis的下拉菜单，在Aggregation中选择average，Field选择tempterature
![](./md_image/dashboard/46.png)

- 打开Buckets X-Axis的下拉菜单，在Aggregation中选择Date Histogram，Field选择datetime。
![](./md_image/dashboard/47.png)

- 点击蓝色的开始按钮就将生成实时图表。
![](./md_image/dashboard/48.png)

