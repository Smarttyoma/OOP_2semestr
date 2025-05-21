from di_container import DependencyInjector
from di_projec.configuration import configure_debug, configure_release
from di_projec.service3 import IService3
from di_projec.service1 import IService1
from di_projec.service2 import IService2
from service1_impl import Service1_Debug

def main():
    print("=== DEBUG CONFIGURATION ===")
    container = DependencyInjector()
    configure_debug(container)

    with container.create_scope():
        s3_1 = container.get_instance(IService3)
        s3_2 = container.get_instance(IService3)
        print(s3_1.execute())
        print(s3_2.execute())

        assert s3_1 is not s3_2
        assert container.get_instance(IService1) is container.get_instance(IService1)
        assert container.get_instance(IService2) is container.get_instance(IService2)

    print("\n=== RELEASE CONFIGURATION ===")
    container = DependencyInjector()
    configure_release(container)

    with container.create_scope():
        s3 = container.get_instance(IService3)
        print(s3.execute())

    print("\n=== FACTORY REGISTRATION ===")
    container = DependencyInjector()
    container.register_factory(IService1, lambda: Service1_Debug())
    print(container.get_instance(IService1).do())

if __name__ == "__main__":
    main()
