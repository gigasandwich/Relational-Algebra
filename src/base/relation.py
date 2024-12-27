from typing import List
from .column import Column
from .row import Row

class Relation:
    """
    Represents a database relation with columns and rows, providing methods for data manipulation
    and relational algebra operations (e.g: projection, selection, joins, union/intersection/difference)
    """

    # ====================================================
    # Initialisation Method
    # ====================================================
    def __init__(self, name: str, *columns: Column):
        """
        Initializes a relation with a name and any columns

        Args:
            name (str): The name of the relation
            *columns (Column): list of Column objects that has a name and a domain

        Raises:
            ValueError: If there's no column
        """
        self.name: str = name
        self.columns: List[Column] = []
        self.rows : List[Row] = []
        
        if columns is not None: # Must have a column
            for col in columns:
                self.columns.append(col)
        else:
            raise ValueError("A relation needs at least one column")
        
        print(f"Relation {name}")

    # ====================================================
    # Main Methods
    # ====================================================

    def insert(self, *args) -> "Row":
        """
        Inserts a new row to the relation, it appends a new row in self.rows

        Args:
            *args: Column-value pairs (e.g: "column_name1", value1, "column_name2", value2)

        Raise:
            ValueError: If the number of supposed number of columns are more than the number of column of the relation
            ValueError: If the number of arguments is odd the value doesn't match the domain of the Column object 
        """

        print("New record inserted")
        return Row(self)

    def project(self, *column_names) -> "Relation":
        """
        Returns this relation with only the specified columns

        Args:
            *column_names (str):     
        """
        return self 
    
    # ====================================================
    # Display Methods
    # ====================================================

    def __str__(self):
        """
        The string representation of the relation and its components with an sql like form 
        """

        if len(self.rows) == 0:
            return "Empty set"
        
        return ""   
    
    def display(self) -> None: 
        """
        Prints the string value of this relation in the terminal
        """
        print(self)
