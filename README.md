# QuModLibsNX13

#### 介绍
适用于网易MC_MOD开发的免费开源框架 (如需摘录部分源代码到其他同类别项目请署名原作者)
交流反馈群: Q494731530


#### NX13变动须知
QuModLibs最初为方便教学小白入门网易MOD开发设计 在早期并未考虑作为正式项目使用
随着该项目的发展 一些过时的代码设计需要迭代 该版本为非向下兼容更新 旧版项目更新前需了解相关改动


#### NX13变动内容
1.所有实体组件类以及EasyThread类被标记为[即将废弃], 移动到Deprecated模块

2.新版实体组件类 QBaseEntityComp 更加安全高性能的实现

3.新的线程模块(包括线程池和主线程通信方案)

4.重构底层源代码实现 (QuMod, Server, Client, LoaderSystem等部分)

5.QuMod模块新增函数式功能

6.移除QuDestroy关键词命名函数

7.新增DestroyFunc装饰器修饰在游戏关闭时执行的函数

8.LensPlayer不再需要开发者释放资源 当播放器不被使用时自动将会释放

9.@Listen 静态注册监听现在将会按照文件module区分隔离了

10.GLR现在支持非玩家实体的节点管理(需声明白名单/全局支持)

11.EventsPool事件池机制 优化高频率动态监听/反监听性能表现

12.新增Util.QTimeLine模块 用于便捷计算关键帧数据

13.新增ModelRender模块处理客户端渲染相关计算


#### 旧版兼容(在未来将会废弃)
如果您想要在旧版项目中使用该版本并确保兼容 请使用Deprecated模块

示例:
from QuModLibs.Modules.Deprecated.Server import *
from QuModLibs.Modules.Deprecated.Client import *

此外QuDestroy关键字命名已被取消 取而代之的是对应的装饰器注册@DestroyFunc