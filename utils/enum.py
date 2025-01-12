from enum import Enum


class ChoicesEnum(Enum):  # for using in models
    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]
