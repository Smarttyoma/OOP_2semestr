WIDTH = 800
HEIGHT = 600


class Point2d:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        if 0 <= value <= WIDTH:
            self._x = value
        else:
            raise ValueError(f"x должно быть в диапазоне [0, {WIDTH}]")

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        if 0 <= value <= HEIGHT:
            self._y = value
        else:
            raise ValueError(f"y должно быть в диапазоне [0, {HEIGHT}]")

    def __eq__(self, other):
        if isinstance(other, Point2d):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return f"Point2d({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()


from math import sqrt


class Vector2d:
    def __init__(self, x: int = 0, y: int = 0, start: Point2d = None, end: Point2d = None):
        if start is not None and end is not None:
            self.x = end.x - start.x
            self.y = end.y - start.y
        else:
            self.x = x
            self.y = y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Индекс должен быть 0 или 1")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Индекс должен быть 0 или 1")

    def __iter__(self):
        return iter((self.x, self.y))

    def __len__(self):
        return 2

    def __eq__(self, other):
        if isinstance(other, Vector2d):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return f"Vector2d({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.x + other.x, self.y + other.y)
        raise TypeError("Можно складывать только объекты Vector2d")

    def __sub__(self, other):
        if isinstance(other, Vector2d):
            return Vector2d(self.x - other.x, self.y - other.y)
        raise TypeError("Можно вычитать только объекты Vector2d")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2d(self.x * scalar, self.y * scalar)
        raise TypeError("Умножение возможно только на число")

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)) and scalar != 0:
            return Vector2d(self.x / scalar, self.y / scalar)
        raise TypeError("Деление возможно только на ненулевое число")

    def dot(self, other):
        if isinstance(other, Vector2d):
            return self.x * other.x + self.y * other.y
        raise TypeError("Скалярное произведение возможно только с Vector2d")

    @staticmethod
    def dot_product(v1, v2):
        if isinstance(v1, Vector2d) and isinstance(v2, Vector2d):
            return v1.x * v2.x + v1.y * v2.y
        raise TypeError("Операция возможна только между объектами Vector2d")

    def cross(self, other):
        if isinstance(other, Vector2d):
            return self.x * other.y - self.y * other.x
        raise TypeError("Векторное произведение возможно только с Vector2d")

    @staticmethod
    def cross_product(v1, v2):
        if isinstance(v1, Vector2d) and isinstance(v2, Vector2d):
            return v1.x * v2.y - v1.y * v2.x
        raise TypeError("Операция возможна только между объектами Vector2d")


# Пример использования
p1 = Point2d(100, 200)
p2 = Point2d(300, 400)
print(p1)  # Point2d(100, 200)

v1 = Vector2d(3, 4)
v2 = Vector2d(start=p1, end=p2)
print(v1)  # Vector2d(3, 4)
print(v2)  # Vector2d(200, 200)
print(abs(v1))  # 5.0

print(v1 + v2)  # Vector2d(203, 204)
print(v1 - v2)  # Vector2d(-197, -196)
print(v1 * 2)  # Vector2d(6, 8)
print(v1 / 2)  # Vector2d(1.5, 2.0)

print(v1.dot(v2))  # 1400
print(Vector2d.dot_product(v1, v2))  # 1400
print(v1.cross(v2))  # 200
print(Vector2d.cross_product(v1, v2))  # 200
