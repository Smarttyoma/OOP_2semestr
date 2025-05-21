from enum import Enum
from types import FunctionType
from contextlib import contextmanager


class LifeStyle(Enum):
    PER_REQUEST = 1
    SCOPED = 2
    SINGLETON = 3


class DependencyInjector:
    def __init__(self):
        self._registrations = {}
        self._singletons = {}
        self._scoped_instances = {}

    def register(self, interface, implementation=None, lifestyle=LifeStyle.PER_REQUEST, params=None):
        self._registrations[interface] = {
            "impl": implementation,
            "lifestyle": lifestyle,
            "params": params or {},
            "factory": None
        }

    def register_factory(self, interface, factory_method):
        self._registrations[interface] = {
            "impl": None,
            "lifestyle": LifeStyle.PER_REQUEST,
            "params": {},
            "factory": factory_method
        }

    def get_instance(self, interface):
        if interface not in self._registrations:
            raise ValueError(f"Interface {interface} not registered")

        reg = self._registrations[interface]
        lifestyle = reg["lifestyle"]

        if lifestyle == LifeStyle.SINGLETON:
            if interface not in self._singletons:
                self._singletons[interface] = self._create_instance(interface)
            return self._singletons[interface]

        elif lifestyle == LifeStyle.SCOPED:
            if interface not in self._scoped_instances:
                self._scoped_instances[interface] = self._create_instance(interface)
            return self._scoped_instances[interface]

        return self._create_instance(interface)

    def _create_instance(self, interface):
        reg = self._registrations[interface]
        if reg["factory"]:
            return reg["factory"]()

        impl = reg["impl"]
        params = reg["params"]

        constructor_args = {}
        for param_name, param_value in params.items():
            if isinstance(param_value, type):  # Dependency
                constructor_args[param_name] = self.get_instance(param_value)
            else:
                constructor_args[param_name] = param_value

        return impl(**constructor_args)

    @contextmanager
    def create_scope(self):
        old_scope = self._scoped_instances.copy()
        self._scoped_instances = {}
        try:
            yield self
        finally:
            self._scoped_instances = old_scope
