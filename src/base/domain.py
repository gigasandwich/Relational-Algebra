from typing import List
from ..constraint.constraint import *

class Domain:
    """
    Represents a set of elements along with some constraints 
    A domain has the same methods as a set in relational algebra context
    """

    # ====================================================
    # Initialisation Method
    # ====================================================

    def __init__(self, allowed_values: List[object] = None, allowed_types: List[type] = None, constraints: List[Constraint] = None):
        """
        Args:
            allowed_values (List[object]): list of objects (e.g: 1, "Fako", True, None)
            allowed_type (List[type]): list of types (e.g: int, str)
        """
        self.allowed_values = allowed_values
        self.allowed_types = allowed_types
        self.constraints = constraints

    # ====================================================
    # Main Methods
    # ====================================================
    
    def union(self, other: "Domain"):
        """
        Creates a new domain which is the result of combining the domain of self and other
        There's no duplicate value

        Args:
            other: The other domain to do union with
        """
        return self
    
    def intersection(self, other: "Domain"):
        """
        Creates a new domain which is the result of crossing the same properties of the domain of self and other
        There's no duplicate value

        Args:
            other: The other domain to do intersection with
        """

        return self
    
    def difference(self, other: "Domain"):
        """
        Creates a new domain which has the properties of self that other doesn't have
        There's no duplicate value

        Args:
            other: The other domain to do diffence with
        """

        return self