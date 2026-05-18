# QuModLibs v1.4
适用于网易MC_MOD开发的免费开源框架 (如需摘录部分源代码到其他同类别项目请署名原作者)。
> 交流反馈群: Q494731530

## 版本说明
当前版本已废弃 `MINI` 精简版，并将部分不常用模块移至 `Optional/Modules` 可选部分；同时移除了内置补全库，完全改为使用系统补全库。

如需旧版的完整包体，请查阅 `release/1.4-full` 分支。

## 创建项目
您可以通过以下步骤创建一个基于`QuModLibs`的网易MCMOD项目。
### 项目结构
推荐放置在 `Scripts/QuModLibs`目录下，但不是必须：
```
├── 行为包
│   └── 脚本目录
│       └── QuModLibs(库目录)
|           ├── __init__.py
|           └── ...
│       ├── __init__.py
│       ├── modMain.py
│       ├── Server.py
│       └── Client.py
```
```python
# modMain.py
# -*- coding: utf-8 -*-
from .QuModLibs.QuMod import * # 导入 QuModLibs.QuMod 的全部功能
myMod = EasyMod()              # 便捷的MOD构建类

# 服务端与客户端注册 将加载: 脚本目录/Server.py 和 脚本目录/Client.py
myMod.Server("Server")
myMod.Client("Client")
```

### 事件监听
通过`@Listen`装饰器注册事件监听。
```python
# Server/Client.py
from .QuModLibs.Server import *
# from .QuModLibs.Client import *

@Listen("OnScriptTickServer")
def OnScriptTickServer(_={}):
    print("game tick")

@Listen("OnCarriedNewItemChangedServerEvent")
def OnCarriedNewItemChangedServerEvent(args={}):
    # type: (dict) -> None
    playerId = args["playerId"] # 触发事件的玩家
    comp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
    comp.SetCommand("/say 我切换了手持物品", playerId)

@DestroyFunc
def onGameClose():
    print("游戏端侧关闭时触发, 等价于Destroy")
```

### RPC通信
通过`@AllowCall`与`Call`实现服务端与客户端的通信。
#### 声明函数
所有需要远程调用的函数必须使用`@AllowCall`装饰器声明。
```python
# Client.py
@AllowCall
def testFunc():
    # 声明的函数将被登记到通信调用中，以便远程调用
    pass
```

#### 调用函数
QuMod提供了封装的`Call`函数用于跨端调用特定函数。
```python
# Server.py
# 服务端需要指定玩家Id调用特定客户端 其中 "*" 作为保留字段用于全体玩家广播
Call(playerId, "testFunc", ...args)
```

#### 批量调用
QuMod提供了封装的`MultiClientsCall`函数可用于批量发包调用。
```python
# MultiClientsCall为服务端独占功能 用于给多个玩家同时发包调用对立客户端函数
# 该方法相比for循环+Call的批量发包性能更好
MultiClientsCall([playerId1, playerId2, ...], "testFunc", ...args)
```

#### 数据包来源
通过使用`@InjectRPCPlayerId`装饰器可在被调用函数中捕获发起调用的玩家Id。
```python
# 服务端独占
from .QuModLibs.Server import *

@AllowCall
@InjectRPCPlayerId
def testFunc(playerId, ...args):
    # playerId为发起调用的玩家Id 会被InjectRPCPlayerId自动插入到第一个参数上
    pass
```
### IMP即初始化
QuMod推崇`import`即初始化的理念，推荐在功能模块加载时完成必要的初始化工作。

### Tools工具模块
`QuModLibs/Tools`提供了一组工具集，可帮助开发者快速实现某些功能，或进行项目优化。

## 更多功能
请参考`QuModLibs`官网文档、讨论群交流，或查看各模块的源代码注释。