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

# ====================================================
# SubClasses
# ====================================================

class NotNullConstraint(Constraint):
    """ 
    This ocnstraint makes sure that any passed object must be not null
    """
    def is_valid(object):
        return object is not None

    # The union/intersection of two "NotNull" constraints is just "NotNull" 
    def union(self, other: Constraint) -> Constraint: 
        if isinstance(other, NotNullConstraint):
            return self
        raise TypeError("Cannot union NotNullConstraint with other types")

    def intersection(self, other):
        if isinstance(other, NotNullConstraint):
            return self 
        raise TypeError("Cannot intersect NotNullConstraint with other types")


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

    def is_valid(self, object):
        if not isinstance(object, str):
            return True
        string = object # for better readability
        return self.min <= len(string) <= self.max

    def union(self, other: "StringLengthConstraint"):
        if isinstance(other, StringLengthConstraint):
            min_len = min(self.min, other.min)
            max_len = max(self.max, other.max)
            return StringLengthConstraint(min_len, max_len)
        raise TypeError("Cannot union StringLengthConstraint with other types")

    def intersection(self, other: "StringLengthConstraint"):
        if isinstance(other, StringLengthConstraint):
            min_len = max(self.min, other.min)
            max_len = min(self.max, other.max)
            if min_len <= max_len:  
                return StringLengthConstraint(min_len, max_len)
            else:
                raise ValueError("No valid intersection between the string lengths")
        raise TypeError("Cannot intersect StringLengthConstraint with other types")


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

    def is_valid(self, object):
        if not isinstance(object, (int, float)):  # Skip validation for non-numeric objects
            return True
        return self.min <= object <= self.max

    def union(self, other):
        if isinstance(other, RangeConstraint):
            # For RangeConstraints, the union will result in two distinct ranges
            if self.max < other.min:  
                return [RangeConstraint(self.min, self.max), RangeConstraint(other.min, other.max)]
            elif other.max < self.min:  
                return [RangeConstraint(other.min, other.max), RangeConstraint(self.min, self.max)]
            else:
                raise ValueError("Range tsy milamina")
        raise TypeError("Cannot union RangeConstraint with other types")

    def intersection(self, other):
        if isinstance(other, RangeConstraint):
            min_val = max(self.min, other.min)
            max_val = min(self.max, other.max)
            if min_val <= max_val: 
                return RangeConstraint(min_val, max_val)
            else:
                raise ValueError("No valid intersection between the ranges")
        raise TypeError("Cannot intersect RangeConstraint with other types")



class PositiveConstraint(Constraint):
    """
    A constraint stating that any number in the allowed types of a domain must be positive
    """
    def __init__(self, max: (int | float) = None):
        self.max = max

    def is_valid(self, value) -> bool:
        if not isinstance(value, (int, float)):
            return False

        if self.max is None:
            return value >= 0
        return 0 <= value <= self.max

    def union(self, other: "Constraint") -> "Constraint":
        if isinstance(other, PositiveConstraint):
            max_value = self.max if self.max is not None and self.max >= other.max else other.max
            return PositiveConstraint(max_value)
        raise TypeError("Cannot union PositiveConstraint with other types")

    def intersection(self, other: "Constraint") -> "Constraint":
        """
        The max value for a PositiveConstraint is the smaller one (None represents infinite here)
        any value < None in this case 
        """
        if isinstance(other, PositiveConstraint):
            if self.max is None: 
                max_value = other.max 
            if max_value is None:
                max_value = self.max

            if self.max < other.max:
                max_value = self.max 
                
            return PositiveConstraint(max_value)  
        raise TypeError("Cannot intersect PositiveConstraint with other types")


