from typing import List
from ..constraint.constraint import *

class Domain:
    """
    Represents a set of elements along with some constraints 
    A domain has the same methods as a set in relational algebra context (union, intersection, difference)
    """

    # ====================================================
    # Initialisation Method
    # ====================================================

    def __init__(self, allowed_values: List[object] = None, allowed_types: List[type] = None, constraints: List[Constraint] = None):
        """
        Args:
            allowed_values: e.g: 1, "Fako", True, None
            allowed_type: e.g: int, str
            constraints: e.g: PositiveConstraint(100), NotNullConstraint()
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
        """
        # For null values
        if value is None:
            if None in self.allowed_values:
                return True
            
            if NotNullConstraint in self.constraints:
                raise ValueError("Value cannot be null.")


        # Check allowed values
        if value in self.allowed_values:
            return True

        # Check allowed types
        for type_ in self.allowed_types:
            if isinstance(value, type_):
                # Check constraints validity
                for constraint in self.constraints:
                    if not constraint.is_valid(value):
                        try:
                            constraint.is_valid(value)
                        except ValueError as e:
                            raise e  # Re-raise the exception with the error message
                    
                return True
        
        raise ValueError(f"Invalid value: {value}.\nAllowed values are: {self.allowed_values},\nAllowed types are: {self.allowed_types}.")

    

    def union(self, other: "Domain") -> "Domain":
        allowed_values = list(set(self.allowed_values) | set(other.allowed_values))
        allowed_types = list(set(self.allowed_types) | set(other.allowed_types))
        constraints = self.merge_constraints(other, "union")
        return Domain(allowed_values, allowed_types, constraints)

    def intersection(self, other: "Domain") -> "Domain":
        allowed_values = list(set(self.allowed_values) & set(other.allowed_values))
        allowed_types = list(set(self.allowed_types) & set(other.allowed_types))
        constraints = self.merge_constraints(other, "intersection")
        return Domain(allowed_values, allowed_types, constraints)

    def difference(self, other: "Domain") -> "Domain":
        allowed_values = list(set(self.allowed_values) - set(other.allowed_values))
        allowed_types = list(set(self.allowed_types) - set(other.allowed_types))
        constraints = self.merge_constraints(other, "difference")
        return Domain(allowed_values, allowed_types, constraints)

    def merge_constraints(self, other: "Domain", operation: str) -> List[Constraint]:
        merged_constraints = []
        for c1 in self.constraints:
            for c2 in other.constraints:
                if isinstance(c1, type(c2)):
                    if operation == "union":
                        merged_constraints.append(c1.union(c2))
                    elif operation == "intersection":
                        merged_constraints.append(c1.intersection(c2))
                    elif operation == "difference":
                        merged_constraints.append(c1.difference(c2))
        return merged_constraints
    
    def __str__(self):
        return f"Domain(allowed_values={self.allowed_values}, allowed_types={self.allowed_types}, constraints={self.constraints})"
