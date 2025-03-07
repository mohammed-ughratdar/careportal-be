from enum import Enum

class Type_of_Care(str, Enum):
    STATIONARY = "stationary"
    AMBULATORY = "ambulatory"
    DAY_CARE = "day care"

