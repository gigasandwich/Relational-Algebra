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
        
        print(f"Relation {name} created")

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
            raise ValueError(f"There should be only {normal_column_numbers}, instead there are {column_numbers - normal_column_numbers} more")
        
        # No column without value
        if args_length%2 != 0:
            raise ValueError(f"Expected: {args_length+1} arguments instead of just{args_length}")

        row = Row(self)
        # Step 1: separating the pair of key-values
        for i in range (0, args_length, 2):
            column_name = args[i]
            value = args[i+1]
            specific_column = self.get_column_by_name(column_name)


            if row in self.rows:
                raise ValueError("This row already exist")

            # Not existing column
            if specific_column is None:
                raise ValueError(f"Column {column_name} doesn't exist")

            # Step 2: checking if each value inserted match the domain of the column
            if not specific_column.is_valid(value):
                raise ValueError(f'Invalid value for column "{column_name}": {value}')

            row.add_value(column_name, value)

        self.rows.append(row)

        print("New record inserted")
        return Row(self)


    def project(self, *col_names) -> "Relation":
        """
        Returns this relation with only the specified columns

        Args:
            *col_names (str): The only columns no be displayed 
        """

        return self

    # ====================================================
    # Helper Methods
    # ====================================================

    def get_column_by_name(self, name) -> Column: 
        for column in self.columns:
            if name == column.name:
                return column
        return None
    
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
            # Maximum length of the column name
            max_name_length = len(col_name)

            # Maximum length of the values in the column
            max_value_length = max( (len(str(row.data.get(col_name, "")) ) for row in self.rows), default = 0)

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
        """
        Prints the string value of this relation in the terminal
        """
        print(self)

