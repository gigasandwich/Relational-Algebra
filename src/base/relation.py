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
        
        if columns is not None: 
            for col in columns:
                self.columns.append(col)
       
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
            ValueError: If that row already exist
        """


        # Error handling
        args_length = len(args) # The number of passed argument

        column_numbers = args_length/2 # The supposed number of columns passed as argument
        normal_column_numbers = len(self.columns)

        # No excess of column
        if(column_numbers > normal_column_numbers):
            raise ValueError(f"Max column number: {normal_column_numbers}, however there are {column_numbers - normal_column_numbers} in the insert statement")
        
        # No column without value
        if args_length%2 != 0:
            raise ValueError(f"Expected: {args_length+1} arguments instead of just {args_length}")

        row = Row(self)
        # Step 1: separating the pair of key-values
        for i in range(0, args_length, 2):
            column_name = args[i]
            value = args[i+1]
            specific_column = self.get_column_by_name(column_name)

            if row in self.rows:
                raise ValueError("This row already exist")

            if specific_column is None:
                raise ValueError(f"Column {column_name} doesn't exist")

            # Step 2: checking if each value inserted match the domain of the column
            if not specific_column.is_valid(value):
                raise ValueError(f'Invalid value for column "{column_name}": {value}') # TODO: print the actual invalidity

            row.add_value(column_name, value)

        self.rows.append(row)
        return Row(self)


    def project(self, *col_names: str) -> "Relation":
        """
        Returns this relation with only the specified columns

        Raises: 
            ValueError: invalid column 
        """
        new_relation = self.copy() # Creating a copy to evit pointer errors
        
        # Step 1: Regrouping the Column objects that are requested
        needed_cols = []
        for col_name in col_names:
            if new_relation.get_column_by_name(col_name) is None: 
                raise ValueError(f"Column {col_name} doesn't exist")
            needed_cols.append(self.get_column_by_name(col_name))
 
        # Step 2: Regrouping the Column objects that aren't needed
        not_needed_cols = ( col for col in new_relation.columns if col not in needed_cols )

        # Step 3: a copy of the original relation without the not needed columns (removing the mapping in the rows too)
        for not_needed_col in not_needed_cols:
            new_relation.columns.remove(not_needed_col)
            for row in new_relation.rows:
                row.data.pop(not_needed_col.name)

        return new_relation
    
    
    def select(self, condition: str)-> "Relation":
        """
        Eliminates row from the original relation ( those that don't match the condition)
        
        Raise:
            ValueError: syntax error
        """
        copy = self.copy()
        new_relation = Relation(f"{copy.name} where: {condition}", *copy.columns)
        for row in copy.rows: 
            if row.evaluate_condition(condition):
                new_relation.rows.append(row)
        return new_relation


    # ====================================================
    # Helper Methods
    # ====================================================

    def get_column_by_name(self, name) -> Column: 
        for column in self.columns:
            if name == column.name:
                return column
        return None
    
    def copy(self) -> "Relation":
        new_relation = Relation(self.name, *self.columns.copy()) # Don't forget the * before self.columns.copy()
        new_relation.rows = self.rows.copy()
        return new_relation

    
    # ====================================================
    # Display Methods
    # ====================================================

    def __str__(self):
        """
        The string representation of the relation and its components with an sql like form 
        """
        
        if len(self.rows) == 0:
            return "Empty set"
        
        col_names = [ col.name for col in self.columns]
        col_widths = []

        for col_name in col_names:
            max_name_length = len(col_name) # Maximum length of the column name
            max_value_length = max( (len(str(row.data.get(col_name, "")) ) for row in self.rows), default = 0) # Maximum length of the values in the column

            # The column width is the larger between max_name and max_value
            col_widths.append(max(max_name_length, max_value_length))

            # Create the horizontal border
            border = "+-" + "-+-".join("-" * width for width in col_widths) + "-+"

            # The header row
            header = "| " + " |".join( col.ljust(width) for col, width in zip(col_names, col_widths)) + " |"

            # The data rows
            data_rows = ["| " + " |".join(str(row.data.get(col, "")).ljust(width) 
                        for col, width in zip(col_names, col_widths)) + " |" 
                        for row in self.rows
            ]

        return "\n".join([border, header, border] + data_rows + [border])
    

    def display(self) -> None: 
        print(self)

