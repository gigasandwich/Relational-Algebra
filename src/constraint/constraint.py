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

    @abstractmethod
    def union(self, other: "Constraint") -> "Constraint":
        pass

    @abstractmethod
    def intersection(self, other: "Constraint") -> "Constraint":
        pass

    @abstractmethod
    def difference(self, other: "Constraint") -> "Constraint":
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
    
    def union(self, other: "Constraint") -> "Constraint":
        return NotNullConstraint()

    def intersection(self, other: "Constraint") -> "Constraint":
        return NotNullConstraint()

    def difference(self, other: "Constraint") -> "Constraint":
        return NotNullConstraint()
    
    def __repr__(self):
        return "NotNullConstraint()"
    

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
    
    def union(self, other: "StringLengthConstraint") -> "StringLengthConstraint":
        # Union takes the widest range of lengths
        return StringLengthConstraint(min(min(self.min, other.min), self.max), max(self.max, other.max))

    def intersection(self, other: "StringLengthConstraint") -> "StringLengthConstraint":
        # Intersection takes the intersection of the ranges
        return StringLengthConstraint(max(self.min, other.min), min(self.max, other.max))

    def difference(self, other: "StringLengthConstraint") -> "StringLengthConstraint":
        # Difference would be tricky, but can be considered as subtracting the range of the other
        if self.min < other.min:
            return StringLengthConstraint(self.min, min(self.max, other.min))
        elif self.max > other.max:
            return StringLengthConstraint(max(self.min, other.max), self.max)
        else:
            return StringLengthConstraint(self.min, self.max)

    def __repr__(self):
        return f"StringLengthConstraint(min={self.min}, max={self.max})"


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
    
    def union(self, other: "RangeConstraint") -> "RangeConstraint":
        return RangeConstraint(min(self.min, other.min), max(self.max, other.max))

    def intersection(self, other: "RangeConstraint") -> "RangeConstraint":
        return RangeConstraint(max(self.min, other.min), min(self.max, other.max))

    def difference(self, other: "RangeConstraint") -> "RangeConstraint":
        # Difference would be the range that is in self but not in the other
        if self.min < other.min:
            return RangeConstraint(self.min, min(self.max, other.min))
        elif self.max > other.max:
            return RangeConstraint(max(self.min, other.max), self.max)
        else:
            return RangeConstraint(self.min, self.max)

    def __repr__(self):
        return f"RangeConstraint(min={self.min}, max={self.max})"


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
    
    def union(self, other: "PositiveConstraint") -> "PositiveConstraint":
        return PositiveConstraint(max(self.max, other.max) if self.max and other.max else None)

    def intersection(self, other: "PositiveConstraint") -> "PositiveConstraint":
        return PositiveConstraint(max(self.max, other.max) if self.max and other.max else None)

    def difference(self, other: "PositiveConstraint") -> "PositiveConstraint":
        if self.max is not None and other.max is not None:
            return PositiveConstraint(max(self.max, other.max))
        return PositiveConstraint()

    def __repr__(self):
        return f"PositiveConstraint(max={self.max})" if self.max else "PositiveConstraint()"

