"""Store information about operator enums."""


from enum import Enum


class Operator(Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

    def __str__(self):
        return f'{self.value}'
