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
            constraints (List[Constraint]): list of constraint (e.g: PositiveConstraint(100), NotNullConstraint())
        """
        self.allowed_values = allowed_values  if allowed_values is not None else [] # List[object] won't work because it's only for type hints 
        self.allowed_types = allowed_types if allowed_types is not None else [] 
        self.constraints = constraints if constraints is not None else [] 

    # ====================================================
    # Main Methods
    # ====================================================
    
    def is_valid(self, value: object) -> bool:
        """
        Checks if a value is conform to the value of the attributes

        Args: 
            value: The object to be checked
        """
        # For null values
        if value is None:
            if None in self.allowed_values:
                return True
            
            if NotNullConstraint in self.constraints:
                return False
            
            return False
    
        # Check allowed values
        if value in self.allowed_values:
            return True

        # Check allowed types
        for type_ in self.allowed_types:
            if isinstance(value, type_):
                # Check constraints validity
                for constraint in self.constraints:
                    if not constraint.is_valid(value):
                        return False
                    
                return True
        
        return False
    

    def union(self, other: "Domain"):
        """
        Creates a new domain which is the result of combining the domain of self and other
        There's no duplicate value

        Args:
            other: The other domain to do union with
        """
        allowed_types = self.allowed_types | other.allowed_types
        allowed_values = self.allowed_values | other.allowed_values
        constraints = list(self.constraints).union(list(other.constraints)) 

        return Domain(allowed_types, allowed_values, constraints)
    

    def intersection(self, other: "Domain"):
        """
        Creates a new domain which is the result of crossing the same properties of the domain of self and other
        There's no duplicate value

        Args:
            other: The other domain to do intersection with
        """
        allowed_types = self.allowed_types & other.allowed_types        
        allowed_values = self.allowed_values & other.allowed_values 
        constraints = self.constraints.intersection(other.constraints)

        return Domain(allowed_types, allowed_values, constraints)
    