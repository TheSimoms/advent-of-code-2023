from collections import namedtuple
from enum import Enum


Position = namedtuple('Position', ['x', 'y'])


class Direction(Enum):
    R = (1, 0)
    D = (0, 1)
    L = (-1, 0)
    U = (0, -1)
