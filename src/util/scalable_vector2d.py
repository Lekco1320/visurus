from .vector2d import Vector2D, Number, Vector2DLike
from typing    import Union

class Scale:
    ...

NumberOrScale = Union[Number, Scale]

class Scale:
    def __init__(self, ratio: float):
        self._ratio = ratio
    
    @property
    def ratio(self):
        return self._ratio
    
    @ratio.getter
    def ratio(self, value):
        self._ratio = value
    
    def __mul__(self, right: NumberOrScale) -> NumberOrScale:
        if isinstance(right, Scale):
            return Scale(self._ratio * right._ratio)
        return self._ratio * right
    
    def __rmul__(self, left: NumberOrScale) -> NumberOrScale:
        return self.__mul__(left)
    
    def __str__(self):
        return f'{self._ratio}*'
    
    def __repr__(self):
        return f'Scale{{ratio={self._ratio}}}'

class ScalableVector2D(Vector2D):
    def __init__(self, x: NumberOrScale, y: NumberOrScale):
        super().__init__(x, y)
    
    def scale(self, size: Vector2DLike, type: type = int) -> Vector2D:
        x, y = self._x, self._y
        if isinstance(x, Scale):
            x *= size[0]
        if isinstance(y, Scale):
            y *= size[1]
        ret = Vector2D(x, y)
        ret.convert(type)
        return ret
    
    def x_number(self) -> bool:
        return isinstance(self._x, (int, float))
    
    def y_number(self) -> bool:
        return isinstance(self._y, (int, float))
    
    def x_scalable(self) -> bool:
        return isinstance(self._x, Scale)
    
    def y_scalable(self) -> bool:
        return isinstance(self._y, Scale)

    def __repr__(self) -> str:
        return f'ScalableVector2D{{x={repr(self._x)}, y={repr(self._y)}}}'
