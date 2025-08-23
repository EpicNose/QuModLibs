import types


class Ref(object):

    def __init__(self, value):
        self.value = value


class Promise(object):

    def __init__(self, executor):
        self.executor = executor
        self.service = None
        self.finished = False
        self.thenHandler = None
        self.catchHandler = None
        self.value = None

    def __call__(self):
        self.executor(self.resolve, self.reject)

    @staticmethod
    def all(promises):

        def executor(resolve, reject):
            total = Ref(len(promises))
            now = Ref(0)

            def thenHandler(value):
                now.value += 1
                if total.value == now.value:
                    resolve([promise.value for promise in promises])

            def catchHandler(value):
                reject(value)

            for promise in promises:
                promise.then(thenHandler, link=True).catch(catchHandler)

        return Promise(executor)

    @staticmethod
    def any(promises):

        def executor(resolve, reject):
            total = Ref(len(promises))
            now = Ref(0)

            def thenHandler(value):
                resolve(value)

            def catchHandler(value):
                now.value += 1
                if total.value == now.value:
                    reject([promise.value for promise in promises])

            for promise in promises:
                promise.then(thenHandler, link=True).catch(catchHandler)

        return Promise(executor)

    def resolve(self, value=None):
        if self.finished:
            return
        self.finished = True
        self.value = value
        if self.thenHandler or self.catchHandler:
            if self.thenHandler:
                self.thenHandler(value)
            return
        try:
            promise = self.service.send((True, value))
            if isinstance(promise, Promise):
                promise.service = self.service
                promise()
        except StopIteration:
            pass

    def reject(self, value=None):
        if self.finished:
            return
        self.finished = True
        self.value = value
        if self.catchHandler or self.thenHandler:
            if self.catchHandler:
                self.catchHandler(value)
            return 
        try:
            promise = self.service.send((False, value))
            if isinstance(promise, Promise):
                promise.service = self.service
                promise()
        except StopIteration:
            pass

    def then(self, handler, link=False):
        self.thenHandler = handler
        if link:
            return self
        self.executor(self.resolve, self.reject)

    def catch(self, handler, link=False):
        self.catchHandler = handler
        if link:
            return self
        self.executor(self.resolve, self.reject)


def Async(business):
    def wrapper(*args, **kwargs):
        result = business(*args, **kwargs)
        if isinstance(result, types.GeneratorType):
            try:
                promise = next(result)
                if isinstance(promise, Promise):
                    promise.service = result
                    promise()
                    return
                return
            except StopIteration:
                pass
        return result
    wrapper.__name__ = business.__name__
    return wrapper


