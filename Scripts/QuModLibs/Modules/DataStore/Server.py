# -*- coding: utf-8 -*-
from .Core import BaseAutoStoreCls
import mod.server.extraServerApi as serverApi

class ServerAutoStoreCls(BaseAutoStoreCls):
    __IS_CLIENT__ = False

    # __VERSION__ = 1               # 数据版本(默认1), 与存档版本不符时会自动丢弃数据
    # __AUTO_SAVE_INTERVAL__ = 8.0  # 自动保存间隔(默认8秒)
    # __SAVED_FULL_NAME__ = ""      # 自定义存档Key(默认自动生成)

    @classmethod
    def mLoadUserData(cls):
        extraData = serverApi.GetEngineCompFactory().CreateExtraData(serverApi.GetLevelId())
        savedData = extraData.GetExtraData(cls.mGetSavedFullName())
        for k, v in cls.mUnpackClsDatas(savedData).items():
            setattr(cls, k, v)

    @classmethod
    def _mSaveUserData(cls):
        extraData = serverApi.GetEngineCompFactory().CreateExtraData(serverApi.GetLevelId())
        extraData.SetExtraData(cls.mGetSavedFullName(), cls.mPackClsDatas())

    @classmethod
    def _updateOldDataCls(cls, oldDataKey):
        extraData = serverApi.GetEngineCompFactory().CreateExtraData(serverApi.GetLevelId())
        data = extraData.GetExtraData(oldDataKey)
        if data:
            extraData.SetExtraData(oldDataKey, {}) # 清空旧数据
        if not data or not isinstance(data, dict):
            return
        savedData = data["__data__"]    # type: dict
        for k, v in savedData.items():
            setattr(cls, k, v)
    
from ....QuModLibs.Server import QuDataStorage

@QuDataStorage.AutoSave(1)
class DataStore:
    VAR1 = 123
    VAR2 = "Hello"

class NewDataStore(DataStore):
    pass