from di_projec.service2 import IService2

class Service2_Debug(IService2):
    def run(self):
        return "Service2 Debug"

class Service2_Release(IService2):
    def run(self):
        return "Service2 Release"
