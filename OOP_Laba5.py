import json
from dataclasses import dataclass, field
from typing import Protocol, Sequence, Optional, TypeVar, Generic, List, Dict, Any

T = TypeVar('T')


# 1. Класс User
@dataclass(order=True)
class User:
    id: int
    name: str
    login: str
    password: str = field(repr=False)
    email: Optional[str] = None
    address: Optional[str] = None


# 2. Протоколы репозиториев
class IDataRepository(Protocol[T]):
    def get_all(self) -> Sequence[T]:
        ...

    def get_by_id(self, id: int) -> Optional[T]:
        ...

    def add(self, item: T) -> None:
        ...

    def update(self, item: T) -> None:
        ...

    def delete(self, item: T) -> None:
        ...


class IUserRepository(IDataRepository[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]:
        ...


# 3. Реализация DataRepository с JSON
class JsonDataRepository(Generic[T]):
    def __init__(self, filename: str, from_dict: callable, to_dict: callable):
        self.filename = filename
        self.from_dict = from_dict
        self.to_dict = to_dict
        self.items: List[T] = []
        self._load()

    def _load(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.items = [self.from_dict(item) for item in data]
        except FileNotFoundError:
            self.items = []

    def _save(self):
        with open(self.filename, 'w') as f:
            data = [self.to_dict(item) for item in self.items]
            json.dump(data, f, indent=4)

    def get_all(self) -> Sequence[T]:
        return self.items.copy()

    def get_by_id(self, id: int) -> Optional[T]:
        return next((item for item in self.items if getattr(item, 'id') == id), None)

    def add(self, item: T) -> None:
        self.items.append(item)
        self._save()

    def update(self, item: T) -> None:
        for i, existing in enumerate(self.items):
            if getattr(existing, 'id') == getattr(item, 'id'):
                self.items[i] = item
                self._save()
                return
        raise ValueError("Item not found")

    def delete(self, item: T) -> None:
        if item in self.items:
            self.items.remove(item)
            self._save()
        else:
            raise ValueError("Item not found")


# 4. Реализация UserRepository
class UserRepository(JsonDataRepository[User], IUserRepository):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            from_dict=lambda d: User(
                id=d['id'],
                name=d['name'],
                login=d['login'],
                password=d['password'],
                email=d.get('email'),
                address=d.get('address')
            ),
            to_dict=lambda u: {
                'id': u.id,
                'name': u.name,
                'login': u.login,
                'password': u.password,
                'email': u.email,
                'address': u.address
            }
        )

    def get_by_login(self, login: str) -> Optional[User]:
        return next((user for user in self.items if user.login == login), None)


# 5. Протокол AuthService
class IAuthService(Protocol):
    def sign_in(self, user: User) -> None:
        ...

    def sign_out(self) -> None:
        ...

    @property
    def is_authorized(self) -> bool:
        ...

    @property
    def current_user(self) -> User:
        ...


# 6. Реализация AuthService
class FileAuthService(IAuthService):
    def __init__(self, user_repo: IUserRepository, auth_file: str = 'auth.json'):
        self.user_repo = user_repo
        self.auth_file = auth_file
        self._current_user: Optional[User] = None
        self._load_auth()

    def _load_auth(self):
        try:
            with open(self.auth_file, 'r') as f:
                data = json.load(f)
                user_id = data.get('user_id')
                if user_id is not None:
                    self._current_user = self.user_repo.get_by_id(user_id)
        except FileNotFoundError:
            self._current_user = None

    def _save_auth(self):
        data = {'user_id': self._current_user.id if self._current_user else None}
        with open(self.auth_file, 'w') as f:
            json.dump(data, f)

    def sign_in(self, user: User) -> None:
        self._current_user = user
        self._save_auth()

    def sign_out(self) -> None:
        self._current_user = None
        self._save_auth()

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> User:
        if not self._current_user:
            raise ValueError("User not authorized")
        return self._current_user


# 7. Демонстрация работы
if __name__ == "__main__":
    # Инициализация репозитория пользователей
    user_repo = UserRepository('users.json')

    # Инициализация сервиса авторизации
    auth_service = FileAuthService(user_repo)

    # Добавление пользователя
    user1 = User(id=1, name="Alice", login="alice", password="pass123", email="alice@example.com")
    user_repo.add(user1)

    # Авторизация пользователя
    auth_service.sign_in(user1)
    print(f"Авторизован: {auth_service.current_user.name}")

    # Смена пользователя
    user2 = User(id=2, name="Bob", login="bob", password="bobpass", address="City")
    user_repo.add(user2)
    auth_service.sign_in(user2)
    print(f"Новый пользователь: {auth_service.current_user.name}")

    # Автоматическая авторизация при перезапуске
    new_auth_service = FileAuthService(user_repo)
    if new_auth_service.is_authorized:
        print(f"Автоматически авторизован: {new_auth_service.current_user.name}")
    else:
        print("Пользователь не авторизован")

    # Выход из системы
    new_auth_service.sign_out()
    print(f"После выхода: авторизован — {new_auth_service.is_authorized}")