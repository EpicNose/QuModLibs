import mod.client.extraClientApi as clientApi
from ..EventsPool.Client import *
from Core import *

levelId = clientApi.GetLevelId()


def sleep(duration):

    def executor(resolve, reject):
        comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(duration, resolve)

    return Promise(executor)


def requestEvent(name, callBack):
    def _callBack(data):
        callBack(data)
    def destroy():
        POOL_UnListenForEvent(name, _callBack)
        
    POOL_ListenForEvent(name, _callBack)

    return destroy
    

def event(name, callBack, time=60.0):

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
        comp = clientApi.GetEngineCompFactory().CreateGame(levelId)
        comp.AddTimer(time, rejectHandler)

    return Promise(executor)


__all__ = [ "sleep", "event", "Promise", "Async" ]