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
        if object is None:
            raise ValueError("Value cannot be null.")
        return True

class StringLengthConstraint(Constraint):
    """
    Limits the length of any string in the allowed types of a domain 
    """
    def __init__(self, min: int, max: int):   
        self.min = min  
        self.max = max

    def is_valid(self, object):
        if isinstance(object, str):
            if not (self.min <= len(object) <= self.max):
                raise ValueError(f"Expected string length:  [{self.min}, {self.max}]. Reality: {len(object)}.")
        return True


class RangeConstraint(Constraint):
    """
    Limits the interval of any string in the allowed types of a domain 
    """
    def __init__(self, min: float, max: float):   
        self.min = min 
        self.max = max

    """
    Before:
    def is_valid(self, object):
        if not isinstance(object, (int, float)):  # Skip validation for non-numeric objects
        return True
    return self.min <= object <= self.max
    """
    def is_valid(self, object):
        if isinstance(object, (int, float)):  # Skip validation for non-numeric objects
            if not (self.min <= object <= self.max):
                raise ValueError(f"Value must be between {self.min} and {self.max}. Got {object}.")
        return True


class PositiveConstraint(Constraint):
    """
    Makes any number in the allowed types of a domain must be positive
    """
    def __init__(self, max: (int | float) = None):
        self.max = max

    def is_valid(self, value) -> bool:
        if isinstance(value, (int, float)):
            if value < 0:
                raise ValueError("Value must be positive. Got negative value.")
            if self.max is not None and value > self.max:
                raise ValueError(f"Value must be less than or equal to {self.max}. Got {value}.")
        return True

