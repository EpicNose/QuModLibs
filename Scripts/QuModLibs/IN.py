# -*- coding: utf-8 -*-
from Util import SystemSide

IsServerUser = False
ModDirName = SystemSide.__module__.split(".")[0]
QuModLibsPath = SystemSide.__module__[:SystemSide.__module__.rfind(".")]

class RuntimeService:
    _serverSystemList = []
    _clientSystemList = []
    _serverStarting = False
    _clientStarting = False

def getUnderlineModDirName():
    # type: () -> str
    """ 获取下划线MOD目录名称 返回结果与preset内置变量__LQuModName__一致 (仅支持ascii字符串) """
    newStr = []     # type: list[int]
    for i, _charStr in enumerate(ModDirName):
        _char = ord(_charStr)
        if (_char >= 65 and _char <= 90):
            # 大写内容 进行处理
            if i > 0:
                newStr.append(ord("_"))
            newStr.append(_char + (97 - 65))
            continue
        # 常规小写内容 直接追加
        newStr.append(_char)
    return "".join((chr(x) for x in newStr))
