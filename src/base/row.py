from __future__ import annotations # Solution to circular import: from ..base.relation import Relation
from typing import Dict, Any
from ..condition.condition import simplify_and_evaluate

class Tuple:
    """
    The real need of creating a relation: putting and stocking data into it
    """

    # ====================================================
    # Initialisation Method
    # ====================================================

    def __init__(self, relation: "Relation"):
        """
        Initialises the following attributes:
            data (dict): a dictionary/map relating the column name and the value it stores

        Args:
            relation (Relation): so the row object could directly access fields and domains and other rows
        """
        self.relation = relation
        self.data: Dict[str, Any] = {}

        # Putting all the data values "None" by default
        for col in self.relation.fields:
            self.data[col.name] = None

    # ====================================================
    # Main Methods
    # ====================================================

    def evaluate_condition(self, condition) -> bool:
        # Step 1: changing the column names by their real values
        for column_name, value in self.data.items():
            condition = condition.replace(column_name, repr(value))
        return simplify_and_evaluate(condition)
    
    def matches(self, other_tuple, fields):
        """
        Checks if the current tuple matches another tuple based on the provided fields.
        A match occurs when all values for the shared fields are equal.
        """
        for field in fields:
            # Fully qualified names to handle prefixes
            self_value = self.data[f"{self.relation.name}.{field.name}"]
            other_value = other_tuple.data[f"{other_tuple.relation.name}.{field.name}"]
            
            if self_value != other_value:
                return False
        return True

    # ====================================================
    # Helper Methods
    # ====================================================

    def add_value(self, column_name: str, value: object):
        self.data[column_name] = value

    def copy(self) -> "Tuple":
        new_tuple = Tuple(self.relation)
        for column_name in self.data:
            new_tuple.add_value(column_name, self.data[column_name])
        return new_tuple
    
    # ====================================================
    # Display Methods
    # ====================================================
    
    def __str__(self):
        return f"Relation: {self.relation.name}, data: {self.data}"