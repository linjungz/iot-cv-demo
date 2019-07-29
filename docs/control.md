## 指令下发

本实验模拟远程进行车内空调温度控制

### 1. 通过Shadow进行控制指令下发

- 模拟app端发出温度控制指令
- 车端接受指令并进行动作
- 车端将更新后的状态重新上报到车联网平台

#### 演示代码
- car_temperature_app.py  模拟app端
- car_temperature_controller.py 模拟车端温度控制器