from typing import Union

Number = Union[int, float]

class Vector2D:
    ...

Vector2DLike    = Union[Vector2D, tuple[Number, Number]]
Vector2DOrTuple = Union[Vector2D, tuple]

class Vector2D:
    def __init__(self, x: Number, y: Number):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
    def tuple(self):
        return (self._x, self._y)
    
    def convert(self, type: type) -> None:
        if isinstance(self._x, (int, float)):
            self._x = type(self._x)
        if isinstance(self._y, (int, float)):
            self._y = type(self._y)
    
    def __add__(self, other: Vector2DLike) -> 'Vector2D':
        if isinstance(other, Vector2D):
            return Vector2D(self._x + other._x, self._y + other._y)
        else:
            return Vector2D(self._x + other[0], self._y + other[1])
    
    def __radd__(self, other: Vector2DLike) -> 'Vector2D':
        return self.__add__(other)
    
    def __iadd__(self, other: Vector2DOrTuple) -> Vector2DOrTuple:
        if isinstance(other, Vector2D):
            return self.__add__(other)
        return self.tuple() + other
    
    def __sub__(self, other: Vector2DLike) -> 'Vector2D':
        if isinstance(other, Vector2D):
            return Vector2D(self._x - other._x, self._y - other._y)
        else:
            return Vector2D(self._x - other[0], self._y - other[1])
    
    def __rsub__(self, other: Vector2DLike) -> 'Vector2D':
        return self.__sub__(other)
    
    def __mul__(self, other: Number) -> 'Vector2D':
        if isinstance(other, Vector2D):
            return Vector2D(self._x * other._x, self._y * other._y)
        return Vector2D(self._x * other, self._y * other)
    
    def __rmul__(self, other: Number) -> 'Vector2D':
        return self.__mul__(other)
    
    def __getitem__(self, key: int) -> Number:
        if key == 0:
            return self._x
        if key == 1:
            return self._y
        raise IndexError('Index is out of range.')
    
    def __setitem__(self, key: int, value: Number) -> None:
        if key == 0:
            self._x = value
        if key == 1:
            self._y = value
        raise IndexError('Index is out of range.')
    
    def __iter__(self):
        return iter(self.tuple())
    
    def __len__(self) -> int:
        return 2
    
    def __str__(self) -> str:
        return f'({self._x}, {self._y})'

    def __repr__(self) -> str:
        return f'Vector2D{{x={self._x}, y={self._y}}}'
