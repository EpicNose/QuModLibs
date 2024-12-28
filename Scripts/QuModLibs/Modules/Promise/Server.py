import mod.server.extraServerApi as serverApi
from ..EventsPool.Server import *
from Core import *

levelId = serverApi.GetLevelId()


def sleep(duration):

    def executor(resolve, reject):
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(duration, resolve)

    return Promise(executor)


def requestEvent(name, callBack):
    def _callBack(data):
        callBack(data)
    def destroy():
        POOL_UnListenForEvent(name, _callBack)
        
    POOL_ListenForEvent(name, _callBack)

    return destroy
    

def event(name, callBack, time=5.0):

    def executor(resolve, reject):

        funcRef = Ref(lambda : None)

        def eventCallBack(args):
            if callBack(args):
                funcRef.value()
                resolve(args)

        def rejectHandler():
            funcRef.value()
            reject()

        funcRef.value = requestEvent(name, eventCallBack)
        comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time, rejectHandler)

    return Promise(executor)


__all__ = [ "sleep", "event", "Promise", "Async" ]