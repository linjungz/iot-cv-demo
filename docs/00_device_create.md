---
layout: post
title:  "用Cloud9创建IoT设备"
toc: true


---
## 1 使用Cloud Formation生成IoT设备

- 请点击此GitHub[链接](https://github.com/linjungz/cloud9/blob/master/README.md)使用我们提供的Cloud Formation模板，请点击北京区域或者宁夏区域的Launch Stack。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/code/a.png">
</a>

![Hello](./md_image/code/a.png)

模板将会启动一台EC2，并配置好Cloud9（云IDE）方便您管理您的IoT设备。点击链接后请登陆您的AWS账号，之后在创建堆栈界面点击创建堆栈。请记住参数中的c9 username以及c9 password，您之后将使用这两个参数登陆Cloud9。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/code/0.png">
</a>

![Hello](./md_image/code/0.png)

- 之后您将在CloudFormation控制台看到堆栈：Cloud9的创建信息，等待状态变成CREATE_COMPLETE
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/code/1.png">
</a>

![Hello](./md_image/code/1.png)

- 在堆栈输出的Cloud9的键对应的值将会是您的Cloud9链接，点击链接并确保公司VPN是关闭的，否则您将无法访问8181端口。在弹出的登陆窗中输入您刚才记住的c9 username以及c9 password。如果忘记了可在堆栈的参数中看到。
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/code/2.png">
</a>

![Hello](./md_image/code/2.png)

<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/code/2a.png">
</a>

![Hello](./md_image/code/2a.png)

- 进入页面后您将看到一个云IDE，下方有一个终端，左方的workspace可以看到您现有的文件
<a data-fancybox="gallery" href="https://iot-demo-resource.s3-ap-southeast-1.amazonaws.com/code/2b.png">
</a>

![Hello](./md_image/code/2b.png)
