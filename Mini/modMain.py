# -*- coding: utf-8 -*-
from QuModLibs.QuMod import *

miniMod = EasyMod()

# 以下是简单的前置MOD关联演示
def hasMainMod():
    # 是否包含前置MOD(实际业务请按需修改)
    return True

@PRE_SERVER_LOADER_HOOK
def SERVER_LOADER():
    if hasMainMod():
        miniMod.Server("Server")

@PRE_CLIENT_LOADER_HOOK
def CLIENT_LOADER():
    if hasMainMod():
        miniMod.Client("Client")