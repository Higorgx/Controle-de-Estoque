from enum import Enum

class RoleEnum(str, Enum):
    administrador = "1"
    suporte = "2"
    gerente = "3"
    usuario = "4"

    @classmethod
    def from_value(cls, value):
        return cls(value).value