from enum import Enum
from util import Vector2D, ScalableVector2D

_HALIGN_ANNOTATIONS = {
    'LEFT'  : '左对齐',
    'CENTER': '居中对齐',
    'RIGHT' : '右对齐',
}

class HorizontalAlignment(Enum):
    LEFT   = 0
    CENTER = 1
    RIGHT  = 2
    
    def __str__(self):
        return _HALIGN_ANNOTATIONS[self.name]

_VALIGN_ANNOTATIONS = {
    'TOP'   : '顶部对齐',
    'CENTER': '居中对齐',
    'BOTTOM': '底部对齐',
}

class VerticalAlignment(Enum):
    TOP    = 0
    CENTER = 1
    BOTTOM = 2
    
    def __str__(self):
        return _VALIGN_ANNOTATIONS[self.name]

class Anchor:
    def __init__(self, position: Vector2D, offset: ScalableVector2D, halign = HorizontalAlignment.LEFT, valign = VerticalAlignment.TOP):        
        self._position = position
        self._offset   = offset
        self._halign   = halign
        self._valign   = valign
    
    @property
    def position(self) -> Vector2D:
        return self._position
    
    @property
    def offset(self) -> ScalableVector2D:
        return self._offset
    
    @property
    def hAilgn(self) -> HorizontalAlignment:
        return self._halign
    
    @property
    def vAlign(self) -> VerticalAlignment:
        return self._valign
    
    def real_position(self, size: tuple[int, int]) -> Vector2D:
        width, height = size
        x, y = self._position
        if   self._halign == HorizontalAlignment.RIGHT:
            x -= width
        elif self._halign == HorizontalAlignment.CENTER:
            x -= width / 2
        if   self._valign == VerticalAlignment.BOTTOM:
            y -= height
        elif self._valign == VerticalAlignment.CENTER:
            y -= height / 2
        return Vector2D(int(x), int(y))
