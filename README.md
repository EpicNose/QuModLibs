# QuModLibs NX14
适用于网易MC_MOD开发的免费开源框架 (如需摘录部分源代码到其他同类别项目请署名原作者)
> 交流反馈群: Q494731530

#### NX14变动内容(08/23)
    - 移除过时的NX12兼容模块
    - 移除过时的CTRender扩展
    - 移除UIManager现推荐直接使用push界面管理
    - AutoSave列为废弃清单(未来将由其他模块替代)
    - EasyScreenNodeCls列为废弃清单(NX15中彻底删除)
    - ItemService现在是单独的模块(Items)不再是Services的子集
    - QAnimManager新增bindRAIINode 自适应绑定方案
    - 调整QuModLibs内部所有相对导入部分，更加标准化
    - Tools/QuModPurge.exe工具支持新版本同时兼容NX13
    - 摄像机运镜系统支持z轴，并调整了局部实现
    - 其他若干小的调整和修复

### Tools工具模块
我们提供了一些工具模块以便加速项目开发 如果您有兴趣也可以尝试使用
其中QuPresets以及相关工具为工业化流水线生成提供帮助 用于快速的封装/引用一个预设