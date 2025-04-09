from enum import Enum

class TipoEnum(int, Enum):
    fisica = 1
    juridica = 2
    
    @classmethod
    def from_value(cls, value):
        return cls(value).value