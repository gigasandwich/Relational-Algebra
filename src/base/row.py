from __future__ import annotations # Solution to circular import: from ..base.relation import Relation
from typing import Dict, Any
from ..condition.condition import simplify_and_evaluate

class Row:
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
            relation (Relation): so the row object could directly access columns and domains and other rows
        """
        self.relation = relation
        self.data: Dict[str, Any] = {}

        # Putting all the data values "None" by default
        for col in self.relation.columns:
            self.data[col.name] = None

    # ====================================================
    # Main Methods
    # ====================================================

    def evaluate_condition(self, condition) -> bool:
        # Step 1: changing the column names by their real values
        for column_name, value in self.data.items():
            condition = condition.replace(column_name, repr(value))
        return simplify_and_evaluate(condition)

    # ====================================================
    # Helper Methods
    # ====================================================

    def add_value(self, column_name: str, value: object):
        self.data[column_name] = value

    def copy(self) -> "Row":
        new_row = Row(self.relation)
        for column_name in self.data:
            new_row.add_value(column_name, self.data[column_name])
        return new_row