from abc import ABC, abstractmethod

# ====================================================
# Interface
# ====================================================

class Constraint(ABC):
    """
    Limits what a domain can apply in its types and values
    """

    """
    Checks if the object is conform to the constraint this class imposes
    """
    @abstractmethod
    def is_valid(object: object) -> bool:
        pass


# ====================================================
# SubClasses
# ====================================================

class NotNullConstraint(Constraint):
    """ 
    This constraint makes sure that any passed object must be not null
    """
    def is_valid(object):
        return object is not None

class StringLengthConstraint(Constraint):
    """
    Limits the length of any string in the allowed types of a domain 
    """
    def __init__(self, min: int, max: int):   
        self.min = min  
        self.max = max

    def is_valid(self, object):
        if not isinstance(object, str):
            return True
        string = object # for better readability
        return self.min <= len(string) <= self.max


class RangeConstraint(Constraint):
    """
    Limits the interval of any string in the allowed types of a domain 
    """
    def __init__(self, min: float, max: float):   
        self.min = min 
        self.max = max

    def is_valid(self, object):
        if not isinstance(object, (int, float)):  # Skip validation for non-numeric objects
            return True
        return self.min <= object <= self.max


class PositiveConstraint(Constraint):
    """
    Makes any number in the allowed types of a domain must be positive
    """
    def __init__(self, max: (int | float) = None):
        self.max = max

    def is_valid(self, value) -> bool:
        if not isinstance(value, (int, float)):
            return False

        if self.max is None:
            return value >= 0
        return 0 <= value <= self.max

