from abc import ABC, abstractmethod
from typing import List, Any


# 1. Протокол слушателя изменений свойства
class IPropertyChangedListener(ABC):
    @abstractmethod
    def on_property_changed(self, obj: Any, property_name: str) -> None:
        pass


# 2. Протокол для управления слушателями изменений
class INotifyDataChanged(ABC):
    @abstractmethod
    def add_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass

    @abstractmethod
    def remove_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass


# 3. Базовый класс с уведомлениями об изменениях
class ObservableModel(INotifyDataChanged):
    def __init__(self):
        self._changed_listeners: List[IPropertyChangedListener] = []

    def add_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        self._changed_listeners.append(listener)

    def remove_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        self._changed_listeners.remove(listener)

    def _notify_property_changed(self, property_name: str) -> None:
        for listener in self._changed_listeners:
            listener.on_property_changed(self, property_name)


# 4. Протокол слушателя валидации изменений /
class IPropertyChangingListener(ABC):
    @abstractmethod
    def on_property_changing(self, obj: Any, property_name: str,
                             old_value: Any, new_value: Any) -> bool:
        pass


# 5. Протокол для управления валидаторами
class INotifyDataChanging(ABC):
    @abstractmethod
    def add_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        pass

    @abstractmethod
    def remove_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        pass


# 6. Расширенный класс с валидацией изменений
class ValidatableModel(ObservableModel, INotifyDataChanging):
    def __init__(self):
        super().__init__()
        self._changing_listeners: List[IPropertyChangingListener] = []

    def add_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        self._changing_listeners.append(listener)

    def remove_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        self._changing_listeners.remove(listener)

    def _validate_property_change(self, property_name: str,
                                  old_value: Any, new_value: Any) -> bool:
        for listener in self._changing_listeners:
            if not listener.on_property_changing(self, property_name, old_value, new_value):
                return False
        return True


# 7. Реализация демонстрационного класса
class Person(ValidatableModel):
    def __init__(self):
        super().__init__()
        self._name: str = ""
        self._age: int = 0

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if self._validate_property_change("name", self._name, value):
            old = self._name
            self._name = value
            self._notify_property_changed("name")

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if self._validate_property_change("age", self._age, value):
            old = self._age
            self._age = value
            self._notify_property_changed("age")


# 8. Реализации слушателей и валидаторов
class DataChangeLogger(IPropertyChangedListener):
    def on_property_changed(self, obj: Any, property_name: str) -> None:
        print(f"[Изменение] Свойство {property_name} объекта {type(obj).__name__} изменено")


class PositiveNumberValidator(IPropertyChangingListener):
    def on_property_changing(self, obj: Any, property_name: str,
                             old_value: Any, new_value: Any) -> bool:
        if isinstance(new_value, (int, float)) and new_value < 0:
            print(f"[Валидация] {property_name} не может быть отрицательным!")
            return False
        return True


class NameLengthValidator(IPropertyChangingListener):
    def on_property_changing(self, obj: Any, property_name: str,
                             old_value: Any, new_value: Any) -> bool:
        if property_name == "name" and len(new_value) < 3:
            print(f"[Валидация] Имя должно быть не короче 3 символов!")
            return False
        return True


# 9. Демонстрация работы
if __name__ == "__main__":
    print("Создаем объект Person...")
    person = Person()

    # Добавляем слушателей
    logger = DataChangeLogger()
    person.add_property_changed_listener(logger)

    # Добавляем валидаторы
    number_validator = PositiveNumberValidator()
    name_validator = NameLengthValidator()
    person.add_property_changing_listener(number_validator)
    person.add_property_changing_listener(name_validator)

    # Тестовые изменения
    print("\nПопытка установить возраст -5:")
    person.age = -5  # Будет отклонено

    print("\nПопытка установить имя 'Al':")
    person.name = "Al"  # Будет отклонено

    print("\nУстанавливаем корректные значения:")
    person.name = "Alice"
    person.age = 25

    print("\nТекущее состояние:")
    print(f"Имя: {person.name}, Возраст: {person.age}")