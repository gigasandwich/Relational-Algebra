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

    """
    Each Constraint class needs these methods below 
    because a the method of a domain with another domain imply that specific method of its constraint with the other's constraint
    """
    @abstractmethod
    def union(other: "Constraint") -> "Constraint":
        pass 
    
    @abstractmethod
    def intersection(other: "Constraint") -> "Constraint":
        pass 

    @abstractmethod
    def difference(other: "Constraint") -> "Constraint":
        pass 


# ====================================================
# SubClasses
# ====================================================

class NotNullConstraint(Constraint):
    """

    """
    def is_valid(object):
        return super().is_valid()

    def union(other):
        return super().union()

    def intersection(other):
        return super().intersection()

    def difference(other):
        return super().difference()

class StringLengthConstraint(Constraint):
    """
    A constraint limiting the length of any string in the allowed types of a domain 
    """
    def __init__(self, min: int, max: int):   
        """
        Args:
            min/max: an integer representing the minimum/maximum length of the string to be evaluated
        """
        self.min = min  
        self.max = max

    def is_valid(object):
        return super().is_valid()

    def union(other):
        return super().union()

    def intersection(other):
        return super().intersection()

    def difference(other):
        return super().difference()


class RangeConstraint(Constraint):
    """
    A constraint limiting the interval of any string in the allowed types of a domain 
    """
    def __init__(self, min: float, max: float):   
        """
        Args:
            min/max: limits of the interval
        """
        self.min = min 
        self.max = max

    def is_valid(object):
        return super().is_valid()

    def union(other):
        return super().union()

    def intersection(other):
        return super().intersection()

    def difference(other):
        return super().difference()


class PositiveConstraint(Constraint):
    """
    A constraint stating that any number in the allowed types of a domain must be positive
    """
    def __init__(self, max: float = None):
        self.max = max

    def is_valid(object):
        return super().is_valid()

    def union(other):
        return super().union()

    def intersection(other):
        return super().intersection()

    def difference(other):
        return super().difference()

