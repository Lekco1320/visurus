from typing import *

class Field:
    @overload
    def __init__(self, name: str) -> None:
        ...
    
    @overload
    def __init__(self, name: str, default: Any) -> None:
        ...
    
    @overload
    def __init__(self, name: str, default: Any, predicate: Callable) -> None:
        ...
    
    def __init__(self, name: str, default: Any = None, predicate: Callable = None) -> None:
        self._name      = name
        self._default   = default
        self._predicate = predicate
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def default(self) -> Any:
        return self._default
    
    @property
    def predicate(self) -> Callable:
        return self._predicate
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Field):
            return self._name == value._name and \
                   self._default == value._default and \
                   self._predicate == value._predicate
        return False
    
    def __hash__(self) -> int:
        hash(self._name) ^ hash(self._default) ^ hash(self._predicate)

class Config:
    def __init__(self, name: str) -> None:
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    def validate(self, fields: list[Field]) -> bool:
        ret = False
        all = set(self.__dict__.keys())
        for field in fields:
            name = field.name
            if hasattr(self, name):
                value = getattr(self, name)
                if isinstance(value, Config):
                    if self.self_validate():
                        ret = True
                elif callable(field.predicate) and field.predicate(value) or \
                     not isinstance(value, type(field.default)):
                    ret = True
            else:
                ret = True
            if ret:
                setattr(self, name, field.default)
            all.discard(name)
        for other in all:
            if other.startswith('_'):
                continue
            delattr(self, other)
            ret = True
        return ret
    
    def self_validate(self) -> bool:
        ...

class AppConfigs:
    def __init__(self, version) -> None:
        self._version = version
        self._configs = dict()
    
    @property
    def version(self) -> str:
        return self._version
    
    def __getitem__(self, name: str) -> Config:
        return self._configs[name]
    
    def __setitem__(self, name: str, value: Config):
        self._configs[name] = value
    
    def __delitem__(self, name: str):
        del self._configs[name]
    
    def __contains__(self, name: str) -> bool:
        return name in self._configs

__all__ = ["Field", "Config", "AppConfigs"]
