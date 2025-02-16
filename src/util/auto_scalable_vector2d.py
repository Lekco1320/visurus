from .vector2d          import Vector2D, Vector2DLike
from .scalable_vector2d import Scale, ScalableVector2D, NumberOrScale
from typing             import Union

class AutoScale:
    def __str__(self) -> str:
        return "Auto"
    
    def __repr__(self) -> str:
        return "AutoScale"

NumberOrAutoScale = Union[NumberOrScale, AutoScale]

class AutoScalableVector2D(ScalableVector2D):
    def __init__(self, x: NumberOrAutoScale, y: NumberOrAutoScale):
        super().__init__(x, y)
    
    def scale(self, refsize: Vector2DLike, orisize: Vector2DLike, type: type = int) -> Vector2D:
        x, y = self._x, self._y
        if isinstance(x, AutoScale) and isinstance(y, AutoScale):
            x, y = orisize[0], orisize[1]
        else:
            if isinstance(x, Scale):
                x *= refsize[0]
            if isinstance(y, Scale):
                y *= refsize[1]
            if isinstance(x, AutoScale):
                ratio = orisize[0] / orisize[1]
                x = y * ratio
            if isinstance(y, AutoScale):
                ratio = orisize[1] / orisize[0]
                y = x * ratio
        ret = Vector2D(x, y)
        ret.convert(type)
        return ret
    
    def x_auto(self) -> bool:
        return isinstance(self._x, AutoScale)
    
    def y_auto(self) -> bool:
        return isinstance(self._y, AutoScale)
    
    def x_auto_scalable(self) -> bool:
        return self.x_auto() or self.x_scalable()
    
    def y_auto_scalable(self) -> bool:
        return self.y_auto() or self.y_scalable()
    
    def __repr__(self) -> str:
        return f'AutoScalableVector2D{{x={repr(self._x)}, y={repr(self._y)}}}'
