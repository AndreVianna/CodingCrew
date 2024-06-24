from attr import dataclass


@dataclass
class Position:
    line: int
    column: int

    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column