# from typing import Dict
from __future__ import annotations # Solution to circular import: from ..base.relation import Relation
from typing import Dict, Any

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


    # ====================================================
    # Helper Methods
    # ====================================================

    def add_value(self, column_name: str, value: object):
        self.data[column_name] = value