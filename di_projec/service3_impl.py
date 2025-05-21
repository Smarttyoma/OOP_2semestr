from di_projec.service3 import IService3
from di_projec.service1 import IService1
from di_projec.service2 import IService2

class Service3_Debug(IService3):
    def __init__(self, service1: IService1, service2: IService2):
        self.service1 = service1
        self.service2 = service2

    def execute(self):
        return f"[DEBUG EXECUTE] {self.service1.do()} + {self.service2.run()}"

class Service3_Release(IService3):
    def __init__(self, service1: IService1, service2: IService2):
        self.service1 = service1
        self.service2 = service2

    def execute(self):
        return f"[RELEASE EXECUTE] {self.service1.do()} + {self.service2.run()}"
