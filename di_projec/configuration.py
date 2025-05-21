from di_container import LifeStyle
from di_projec.service1 import IService1
from di_projec.service2 import IService2
from di_projec.service3 import IService3
from di_projec.service1_impl import Service1_Debug, Service1_Release
from di_projec.service2_impl import Service2_Debug, Service2_Release
from di_projec.service3_impl import Service3_Debug, Service3_Release

def configure_debug(container):
    container.register(IService1, Service1_Debug, LifeStyle.SINGLETON)
    container.register(IService2, Service2_Debug, LifeStyle.SCOPED)
    container.register(IService3, Service3_Debug, LifeStyle.PER_REQUEST, {
        "service1": IService1,
        "service2": IService2,
    })

def configure_release(container):
    container.register(IService1, Service1_Release, LifeStyle.SINGLETON)
    container.register(IService2, Service2_Release, LifeStyle.SCOPED)
    container.register(IService3, Service3_Release, LifeStyle.PER_REQUEST, {
        "service1": IService1,
        "service2": IService2,
    })
