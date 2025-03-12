# -*- coding: utf-8 -*-
from ...Client import _getLoaderSystem, ListenForEvent, UnListenForEvent, Events
from ..EventsPool.Client import POOL_ListenForEvent, POOL_UnListenForEvent
from ...UI import EasyScreenNodeCls
import weakref
lambda: "UI扩展功能 By Zero123"

class QGridData:
    """ 网格信息 """
    EVENT_NAME = "GridComponentSizeChangedClientEvent"
    def __init__(self, path, isScrollGrid = False, bindFunc = lambda *_: None, bindUpdateBeforeFunc = lambda *_: None, bindUpdateFinishFunc = lambda *_: None, bindGridConName = "", pushUIMode=False):
        # type: (str, bool, object, object, object, str, bool) -> None
        self.path = path
        self.isScrollGrid = isScrollGrid
        self.bindFunc = bindFunc
        self.bindUpdateBeforeFunc = bindUpdateBeforeFunc
        self.bindUpdateFinishFunc = bindUpdateFinishFunc
        self.bindGridConName = bindGridConName
        self._pushUIMode = pushUIMode
        self._gridPathBasedOnScrollView = ""
        self._sharedDict = {}
    
    def setGridPathBasedOnScrollView(self, _path=""):
        """ 设置基于滚动视图的网格路径 (倘若不是直接绑定网格而是有其他父级关系时使用该方法) """
        self._gridPathBasedOnScrollView = _path
        return self
    
    def getRealPath(self, uiNode):
        # type: (EasyScreenNodeCls) -> str
        """ 获取真实路径 """
        if self.isScrollGrid:
            # 对于网格列表则获取一下实时渲染路径
            return uiNode.GetBaseUIControl(self.path).asScrollView().GetScrollViewContentPath() + self._gridPathBasedOnScrollView
        return self.path

    def getRealComponentPath(self, uiNode):
        # type: (EasyScreenNodeCls) -> str
        componentPath = str(getattr(uiNode, "component_path"))
        return componentPath + self.getRealPath(uiNode)
    
    def getPosWithPath(self, _path = ""):
        """ 基于路径获取Pos """
        if self.bindGridConName:
            _path = _path[_path.rfind(self.bindGridConName)+len(self.bindGridConName):]
        count = 0
        _sum = 0
        for _char in _path[::-1]:
            _c = ord(_char)
            if 48 <= _c and 57 >= _c:
                _sum += (10 ** count) * (_c - 48)
                count += 1
                continue
            break
        return _sum

    def childsGen(self, uiNode):
        """ 创建子节点生成器 包含所有已渲染的子节点根级PATH """
        realPath = self.getRealPath(uiNode)
        headPath = ""
        if self._pushUIMode:
            headPath = self.path[:self.path.find("/", 1)]
        for gridPath in uiNode.GetAllChildrenPath(realPath):
            # 通过切片拿到相对路径信息
            if headPath:
                # GetAllChildrenPath在PushUI下拿到的路径并不完整需要重新计算
                gridPath = "{}/{}".format(headPath, gridPath)
            absPath = gridPath[len(realPath):]  # type: str
            if absPath.count("/") == 1:         # 判定为Grid根层级
                yield (self.getPosWithPath(absPath) - 1, gridPath)

    def updateRender(self, uiNode):
        # type: (EasyScreenNodeCls) -> str
        """ 刷新渲染 """
        self.bindUpdateBeforeFunc()
        for index, gridPath in self.childsGen(uiNode):
            try:
                self.bindFunc(gridPath, index)
            except Exception:
                import traceback
                traceback.print_exc()
        self.bindUpdateFinishFunc()

class QUICanvas:
    """ QUI画布绘制类 """
    def __init__(self, uiNode, parentPath = ""):
        # type: (EasyScreenNodeCls, str) -> None
        self._conPath = None
        self._uiNodeRef = weakref.ref(uiNode)
        """ ui节点弱引用 """
        self._parentPath = parentPath
        """ 节点所在父路径 """
        self.drawDefName = ""
        """ 绑定预制件 namespace.controlName """
        self._T_FORCEUPDATE = True
        self._T_JUST_ON_DESTROY = False

    def getNodeLiveState(self):
        # type: () -> bool
        """ 获取节点存活状态 """
        if self.getUiNode():
            return True
        return False
    
    def getParentLiveState(self):
        # type: () -> bool
        """ 获取父节点存活状态 """
        if not self.getNodeLiveState():
            return False
        return self.getUiNode().GetBaseUIControl(self._parentPath) != None

    def getDrawControlLiveState(self):
        # type: () -> bool
        """ 获取绘制节点存活状态 """
        if not self.getNodeLiveState():
            return False
        return self.getUiNode().GetBaseUIControl(self._conPath) != None

    def getUiNode(self):
        """ 获取ui节点(解弱引用) """
        return self._uiNodeRef()

    def rebuildUiNode(self, newUiNode):
        # type: (EasyScreenNodeCls) -> None
        """ 重新绑定uiNode """
        if self._conPath != None:
            raise Exception("已构建控件的对象无法重新绑定UI节点")
        self._uiNodeRef = weakref.ref(newUiNode)

    def rebuildParentPath(self, _newPath):
        # type: (str) -> None
        """ 重新绑定parent """
        if self._conPath != None:
            raise Exception("已构建控件的对象无法重新绑定父路径")
        self._parentPath = _newPath

    def onCreate(self):
        from uuid import uuid4
        uiNode = self.getUiNode()
        uiName = "q"+str(uuid4().hex)
        childNode = uiNode.CreateChildControl(self.drawDefName, uiName, uiNode.GetBaseUIControl(self._parentPath), self._T_FORCEUPDATE)
        self._conPath = childNode.GetPath()

    def onDestroyBefore(self):
        pass

    def onDestroy(self):
        pass

    def getRandomName(self):
        """ 获取随机名称 """
        from uuid import uuid4
        return "q"+str(uuid4().hex)

    def createChildControl(self, drawDefName = "namespace.controlName", conName = "_default", forceUpdate = True):
        """ 动态创建子控件 """
        uiNode = self.getUiNode()
        return uiNode.CreateChildControl(drawDefName, conName, uiNode.GetBaseUIControl(self._parentPath), forceUpdate)

    def clearParent(self):
        """ 清理parent目录所有控件 """
        uiNode = self.getUiNode()
        for realPath in uiNode.GetAllChildrenPath(self._parentPath):
            absPath = realPath[len(self._parentPath):]  # 通过切片拿到相对路径信息
            if absPath.count("/") == 1:                 # 判定为根层级
                uiNode.RemoveComponent(realPath, self._parentPath)

    def listenQGridRender(self, _QGridData):
        # type: (QGridData) -> None
        """ 监听网格渲染 """
        def GridComponentSizeChangedClientEvent(args={}):
            path = str(args["path"])
            uiNode = self.getUiNode()
            if path.endswith(_QGridData.getRealComponentPath(uiNode)):
                _QGridData.updateRender(uiNode)
        from ...Util import RandomUid
        GridComponentSizeChangedClientEvent.__name__ = RandomUid()
        _getLoaderSystem().unsafeUpdate(ListenForEvent(QGridData.EVENT_NAME, self, GridComponentSizeChangedClientEvent))
        _QGridData._sharedDict["listenFun"] = GridComponentSizeChangedClientEvent

    def unListenQGridRender(self, _QGridData):
        # type: (QGridData) -> None
        """ 取消监听网格渲染 """
        UnListenForEvent(QGridData.EVENT_NAME, self, _QGridData._sharedDict["listenFun"])
        _QGridData._sharedDict["listenFun"] = None

    def getBaseUIControl(self):
        """ 获取网易UI控件对象 """
        if not self._conPath:
            return
        return self.getUiNode().GetBaseUIControl(self._conPath)

    def removeControl(self, justOnDestroy = False):
        """ 移除控件 """
        self._T_JUST_ON_DESTROY = justOnDestroy
        if justOnDestroy:
            if self._conPath != None:
                self._conPath = None
                self.onDestroy()
                return True
            return False
        if self._conPath != None:
            self.onDestroyBefore()
            self.getUiNode().RemoveComponent(self._conPath, self._parentPath)
            self._conPath = None
            self.onDestroy()
            return True
        return False
    
    def createControl(self, forceUpdate = True):
        """ 构建控件 """
        if self._conPath != None:
            return
        self._T_FORCEUPDATE = forceUpdate
        self.onCreate()

class QUIControlFuntion(QUICanvas):
    """ QUI控件功能类(继承QUICanvas 但不再创建新控件而是管理已有控件) """
    def onCreate(self):
        self._conPath = self._parentPath
    
    def removeControl(self):
        if self._conPath != None:
            self.onDestroyBefore()
            self._conPath = None
            self.onDestroy()

class QGridBinder(QUIControlFuntion):
    """ 网格绑定器 用于自动化管理界面中的网格/列表网格元素更新处理
        self.gridBinder = QGridBinder(self).setGridData(
            QGridData(...)
        )

        def Create(self):
            self.gridBinder.start()
        
        def Destroy(self):
            self.gridBinder.stop()
    """
    def __init__(self, uiNode, parentPath=""):
        QUIControlFuntion.__init__(self, uiNode, parentPath)
        self._bindGridData = None

    def setGridData(self, gridData):
        # type: (QGridData) -> QGridBinder
        self._bindGridData = gridData
        return self

    def start(self):
        """ 启用绑定器(需手动释放) """
        if not self._bindGridData:
            raise RuntimeError("缺少QGridData绑定 请先通过setGridData绑定管理数据")
        self.createControl()
        return self

    def stop(self):
        """ 停用绑定器(释放) """
        self.removeControl()
        return self

    def updateRender(self):
        """ 主动触发渲染更新 将触发对应的绑定函数 """
        self._bindGridData.updateRender(self.getUiNode())
        return self

    def getRealPath(self):
        """ 获取真实的渲染路径 """
        return self._bindGridData.getRealPath(self.getUiNode())

    def onCreate(self):
        QUIControlFuntion.onCreate(self)
        self.listenQGridRender(self._bindGridData)

    def onDestroy(self):
        QUIControlFuntion.onDestroy(self)
        self.unListenQGridRender(self._bindGridData)

class QUIAutoCanvas(QUICanvas):
    """ QUI智能画布绘制类 """
    def _getIsLive(self):
        return self.getDrawControlLiveState()

    def _onTick(self, _={}):
        if not self._getIsLive():
            self.removeControl(True)
            return
        self.onTick()

    def onTick(self):
        pass

    def onCreate(self):
        QUICanvas.onCreate(self)
        POOL_ListenForEvent(Events.OnScriptTickClient, self._onTick)
    
    def onDestroy(self):
        QUICanvas.onDestroy(self)
        POOL_UnListenForEvent(Events.OnScriptTickClient, self._onTick)

class QUIAutoControlFuntion(QUIControlFuntion):
    """ QUI智能控件功能类 """
    def _getIsLive(self):
        return self.getParentLiveState()

    def _onTick(self, _={}):
        if not self._getIsLive():
            self.removeControl()
            return
        self.onTick()

    def onTick(self):
        pass

    def onCreate(self):
        QUIControlFuntion.onCreate(self)
        POOL_ListenForEvent(Events.OnScriptTickClient, self._onTick)
    
    def onDestroy(self):
        QUIControlFuntion.onDestroy(self)
        POOL_UnListenForEvent(Events.OnScriptTickClient, self._onTick)