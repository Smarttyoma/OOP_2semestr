from di_projec.service1 import IService1

class Service1_Debug(IService1):
    def do(self):
        return "Service1 Debug"

class Service1_Release(IService1):
    def do(self):
        return "Service1 Release"
