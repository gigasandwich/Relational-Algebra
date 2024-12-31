from typing import List, Set
from .column import Field
from .row import Tuple

class Relation:
    """
    Represents a database relation with fields and tuples, providing methods for data manipulation
    and relational algebra operations (e.g: projection, selection, joins, union/intersection/difference)
    """

    # ====================================================
    # Initialisation Method
    # ====================================================
    def __init__(self, name: str, *fields: Field):
        """
        Initializes a relation with a name and any fields

        Args:
            name (str): The name of the relation
            *fields (Field): list of Field objects that has a name and a domain

        Raises:
            ValueError: If there's no field
        """
        self.name: str = name
        self.fields: List[Field] = []
        self.tuples : List[Tuple] = []
        
        if fields is not None: 
            for col in fields:
                self.fields.append(col)
       
    # ====================================================
    # Main Methods
    # ====================================================

    def insert(self, *args) -> "Tuple":
        """
        Inserts a new row to the relation, it appends a new row in self.tuples

        Args:
            *args: Column-value pairs (e.g: "field_name1", value1, "field_name2", value2)

        Raise:
            ValueError: If the number of supposed number of fields are more than the number of column of the relation
            ValueError: If the number of arguments is odd the value doesn't match the domain of the Column object
            ValueError: If that row already exist
        """


        # Error handling
        args_length = len(args) # The number of passed argument

        field_numbers = args_length/2 # The supposed number of fields passed as argument
        normal_field_numbers = len(self.fields)

        # No excess of column
        if field_numbers > normal_field_numbers:
            raise ValueError(f"Max column number: {normal_field_numbers}, however there are {field_numbers - normal_field_numbers} in the insert statement")
        
        # No column without value
        if args_length%2 != 0:
            raise ValueError(f"Expected: {args_length+1} arguments instead of just {args_length}")

        row = Tuple(self)
        # Step 1: separating the pair of key-values
        for i in range(0, args_length, 2):
            field_name = args[i]
            value = args[i+1]
            specific_column = self.get_field_by_name(field_name)

            if row in self.tuples:
                raise ValueError("This row already exist")

            if specific_column is None:
                raise ValueError(f"Column {field_name} doesn't exist")

            try:
                # Step 2: checking if each value inserted match the domain of the column
                if not specific_column.is_valid(value):
                    # We don't reach this because the exception is raised in `is_valid`
                    pass
            except ValueError as e:
                raise ValueError(f'Error validating value for column "{field_name}": {str(e)}')

            row.add_value(field_name, value)

        self.tuples.append(row)
        return Tuple(self)


    def project(self, *col_names: str) -> "Relation":
        """
        Returns this relation with only the specified fields

        Raises: 
            ValueError: invalid column 
        """
        new_relation = self.copy() # Creating a copy to evit pointer errors
        
        # Step 1: Regrouping the Column objects that are requested
        needed_cols = []
        for col_name in col_names:
            if new_relation.get_field_by_name(col_name) is None: 
                raise ValueError(f"Column {col_name} doesn't exist")
            needed_cols.append(self.get_field_by_name(col_name))
 
        # Step 2: Regrouping the Column objects that aren't needed
        not_needed_cols = ( col for col in new_relation.fields if col not in needed_cols )

        # Step 3: a copy of the original relation without the not needed fields (removing the mapping in the tuples too)
        for not_needed_col in not_needed_cols:
            new_relation.fields.remove(not_needed_col)
            for row in new_relation.tuples:
                row.data.pop(not_needed_col.name)

        return new_relation
    
    
    def select(self, condition: str)-> "Relation":
        """
        Eliminates row from the original relation ( those that don't match the condition)
        
        Raise:
            ValueError: syntax error
        """
        copy = self.copy()
        new_relation = Relation(f"{copy.name} where: {condition}", *copy.fields)
        for row in copy.tuples: 
            if row.evaluate_condition(condition):
                new_relation.tuples.append(row)
        return new_relation
    
    
    def cartesian_product(self, other: "Relation") -> "Relation":  
        # Copying to dodge pointer issue  
        copied_self = self.copy_with_renamed_fields(self.name)
        copied_other = other.copy_with_renamed_fields(other.name)

        result_relation = Relation(self.name + " x " + other.name)
        
        for field in copied_self.fields:
            result_relation.add_field(field)

        for field in copied_other.fields:
            result_relation.add_field(field)

        for tuple1 in copied_self.tuples:
            for tuple2 in copied_other.tuples:
                combined_tuple = Tuple(result_relation)
                
                for field in copied_self.fields:
                    combined_tuple.add_value(field.name, tuple1.data[field.name])
                
                for field in copied_other.fields:
                    combined_tuple.add_value(field.name, tuple2.data[field.name])
                
                result_relation.add_tuple(combined_tuple)

        return result_relation

    # ====================================================
    # Inner join methods
    # ====================================================

    def theta_join(self, other: "Relation", condition: str) -> "Relation":
        cartesian_product = self.cartesian_product(other)
        new_relation = cartesian_product.select(condition)
        new_relation.name = self.name + " THETA_JOIN "  + other.name
        return new_relation


    def natural_join(self, other: "Relation", *common_fields: str) -> "Relation":
        """
        Equivalent to equijoin with any fields ????

        Args:
            common_fields [str]: common fields going by pair eg: "pair1a", "pair1b", "pair2a", "pair2b" 
        """

        # Keep the tuple ONLY if field from self is equal to field from other
        condition = " and ".join( f"{self.name}.{common_fields[i]} == {other.name}.{common_fields[i+1]}" for i in range(0, len(common_fields), 2))
        new_relation = self.cartesian_product(other).select(condition)
        new_relation.name = f"{self.name} natural_join {other.name}: {common_fields}"

        # Remove duplicate columns from the second relation
        for i in range(0, len(common_fields), 2):
            field_from_self = new_relation.get_field_by_name(f"{self.name}.{common_fields[i]}")
            field_from_other = new_relation.get_field_by_name(f"{other.name}.{common_fields[i+1]}")
            if field_from_self in new_relation.fields and field_from_other in new_relation.fields:
                new_relation.fields.remove(field_from_other)

        # Remove the self./other. in the name of the columns
        new_relation = new_relation.copy_with_removed_fields(f"{self.name}.")
        new_relation = new_relation.copy_with_removed_fields(f"{other.name}.")

        return new_relation

    def automatic_natural_join(self, other: "Relation") -> "Relation":
        common_fields = [col.name for col in self.fields if col.name in [c.name for c in other.fields]]

        cartesian_product = self.cartesian_product(other)
        condition = " and ".join([f"{self.name}.{col} == {other.name}.{col}" for col in common_fields])
        selected_relation = cartesian_product.select(condition)

        # Remove duplicate fields
        new_relation = Relation(f"{self.name} NATURAL_JOIN {other.name}")
        added_fields = set()
        for field in selected_relation.fields:
            # Skip duplicate fields (from the second relation in common)
            if field.name.split(".")[-1] not in added_fields:
                new_relation.add_field(field)
                added_fields.add(field.name.split(".")[-1])

        new_relation.tuples = selected_relation.tuples

        # Remove the self./other. in the name of the columns
        new_relation = new_relation.copy_with_removed_fields(f"{self.name}.")
        new_relation = new_relation.copy_with_removed_fields(f"{other.name}.")
        
        return new_relation
    
    def equi_join(self, other: "Relation", field1, field2) -> "Relation":
        condition = f"{self.name}.{field1} == {other.name}.{field2}"
        return self.theta_join(other, condition)

    # ====================================================
    # Outter join methods
    # ====================================================

    def outer_join(self, other: "Relation", condition: str) -> "Relation":
        """
        Performs a full outer join between two relations based on a condition.
        """
        theta_join = self.theta_join(other, condition)
        
        self_relation = self.copy_with_renamed_fields(self.name)
        other_relation = other.copy_with_renamed_fields(other.name)

        result_relation = Relation(f"{self.name} FULL OUTER JOIN {other.name}")
        result_relation.fields = self_relation.fields + other_relation.fields  

        # Add matched tuples from the condition of the theta join
        result_relation.tuples.extend(theta_join.tuples)

        # Identify unmatched rows from the left relation (self)
        unmatched_left = []
        for row in self_relation.tuples:
            # Check if the row from self matches any row from the theta_join
            matched = False
            for matched_row in theta_join.tuples:
                if all(
                    row.data[f"{field.name}"] == matched_row.data[f"{field.name}"]
                    for field in self_relation.fields
                ):
                    matched = True
                    break
            if not matched:
                unmatched_left.append(row)

        for row in unmatched_left:
            new_row = Tuple(result_relation)
            # Add the values from the left relation (self)
            for field in self_relation.fields:
                new_row.data[f"{field.name}"] = row.data[field.name]
            # Set None for the unmatched columns from the right relation (other)
            for field in other_relation.fields:
                new_row.data[f"{field.name}"] = None
            result_relation.add_tuple(new_row)

        # Identify unmatched rows from the right relation (other)
        unmatched_right = []
        for row in other_relation.tuples:
            # Check if the row from other matches any row from the theta_join
            matched = False
            for matched_row in theta_join.tuples:
                if all(
                    row.data[f"{field.name}"] == matched_row.data[f"{field.name}"]
                    for field in other_relation.fields
                ):
                    matched = True
                    break
            if not matched:
                unmatched_right.append(row)

        for row in unmatched_right:
            new_row = Tuple(result_relation)
            # Set None for the unmatched columns from the left relation (self)
            for field in self_relation.fields:
                new_row.data[f"{field.name}"] = None
            # Add the values from the right relation (other)
            for field in other_relation.fields:
                new_row.data[f"{field.name}"] = row.data[field.name]
            result_relation.add_tuple(new_row)

        return result_relation



    def left_outer_join(self, other: "Relation", condition: str) -> "Relation":
        """
        Performs a full outer join between two relations based on a condition.
        """
        theta_join = self.theta_join(other, condition)
        
        self_relation = self.copy_with_renamed_fields(self.name)
        other_relation = other.copy_with_renamed_fields(other.name)

        result_relation = Relation(f"{self.name} FULL OUTER JOIN {other.name}")
        result_relation.fields = self_relation.fields + other_relation.fields

        # Add matched tuples from the theta join
        result_relation.tuples.extend(theta_join.tuples)

        # Identify unmatched rows from the left relation (self)
        unmatched_left = []
        for row in self_relation.tuples:
            # Check if the row from self matches any row from the theta_join
            matched = False
            for matched_row in theta_join.tuples:
                if all(
                    row.data[f"{field.name}"] == matched_row.data[f"{field.name}"]
                    for field in self_relation.fields
                ):
                    matched = True
                    break
            if not matched:
                unmatched_left.append(row)

        for row in unmatched_left:
            new_row = Tuple(result_relation)
            # Add the values from the left relation (self)
            for field in self_relation.fields:
                new_row.data[f"{field.name}"] = row.data[field.name]
            # Set None for the unmatched columns from the right relation (other)
            for field in other_relation.fields:
                new_row.data[f"{field.name}"] = None
            result_relation.add_tuple(new_row)

        return result_relation


    """
    The problem with this method is the order of the columns (Reality: the other goes first. Expectation: should be the opposite)
    """
    def right_outer_join(self, other: "Relation", condition: str) -> "Relation":
        return other.left_outer_join(self, condition)

    def right_outer_join(self, other: "Relation", condition: str) -> "Relation":

        # Perform a theta join based on the provided condition
        theta_join = self.theta_join(other, condition)
        
        self_relation = self.copy_with_renamed_fields(self.name)
        other_relation = other.copy_with_renamed_fields(other.name)

        # Create the resulting relation
        result_relation = Relation(f"{self.name} FULL OUTER JOIN {other.name}")
        result_relation.fields = self_relation.fields + other_relation.fields  # Combine the fields from both relations

        # Add matched tuples from the theta join
        result_relation.tuples.extend(theta_join.tuples)

        # Identify unmatched rows from the right relation (other)
        unmatched_right = []
        for row in other_relation.tuples:
            # Check if the row from other matches any row from the theta_join
            matched = False
            for matched_row in theta_join.tuples:
                if all(
                    row.data[f"{field.name}"] == matched_row.data[f"{field.name}"]
                    for field in other_relation.fields
                ):
                    matched = True
                    break
            if not matched:
                unmatched_right.append(row)

        for row in unmatched_right:
            new_row = Tuple(result_relation)
            # Set None for the unmatched columns from the left relation (self)
            for field in self_relation.fields:
                new_row.data[f"{field.name}"] = None
            # Add the values from the right relation (other)
            for field in other_relation.fields:
                new_row.data[f"{field.name}"] = row.data[field.name]
            result_relation.add_tuple(new_row)

        return result_relation

    
    # ====================================================
    # Helper Methods
    # ====================================================

    def get_field_by_name(self, name) -> Field: 
        for field in self.fields:
            if name == field.name:
                return field
        return None
    
    def copy(self) -> "Relation":
        new_relation = Relation(self.name, *self.fields.copy()) # Don't forget the * before self.fields.copy()
        new_relation.tuples = self.tuples.copy()
        return new_relation
    
    def copy_with_renamed_fields(self, prefix: str) -> "Relation":
        new_relation = Relation(self.name)  

        for field in self.fields:
            new_field = Field(prefix + "." + field.name, domain = field.domain)
            new_relation.add_field(new_field)
        
        for row in self.tuples:
            new_row = row.copy()
            for field in self.fields:
                old_field_name = field.name
                new_field_name = prefix + "." + field.name
                new_row.data[new_field_name] = new_row.data.pop(old_field_name)

            new_relation.add_tuple(new_row)

        return new_relation


    def copy_with_removed_fields(self, prefix: str) -> "Relation":
        new_relation = Relation(f"{self.name.removeprefix(prefix)}")
        for field in self.fields:
            new_field = Field(field.name.removeprefix(prefix), domain = field.domain)
            new_relation.add_field(new_field)
        
        for tuple in self.tuples:
            new_tuple = tuple.copy()
            for field in self.fields:
                old_field_name = field.name
                new_field_name = field.name.removeprefix(prefix)
                new_tuple.data[new_field_name] = new_tuple.data.pop(old_field_name)

            new_relation.add_tuple(new_tuple)

        return new_relation
    
    def has_matching_tuple(self, tuple, other: "Relation") -> bool:
        for other_tuple in other.tuples:
            if tuple.equals(other_tuple):
                return True 
        return False

    def add_field(self, field: Field) -> None:
        self.fields.append(field)

    def add_tuple(self, tuple: Tuple):
        self.tuples.append(tuple)

    # ====================================================
    # Display Methods
    # ====================================================

    def __str__(self):
        """
        The string representation of the relation and its components with an SQL-like form.
        """
        if len(self.tuples) == 0:
            return "Empty set"

        field_names = [field.name for field in self.fields]

        field_widths = []
        for field_name in field_names:
            max_name_length = len(field_name) 
            max_value_length = max(
                (len(str(row.data.get(field_name, ""))) for row in self.tuples), 
                default=0
            ) 

            # field width = max(max_name, max_value)
            field_widths.append(max(max_name_length, max_value_length))

        border = "+-" + "-+-".join("-" * width for width in field_widths) + "-+"

        header = "| " + " | ".join(
            field.ljust(width) for field, width in zip(field_names, field_widths)
        ) + " |"

        data_tuples = [
            "| " + " | ".join(
                str(repr(row.data.get(field, ""))).ljust(width) for field, width in zip(field_names, field_widths) # Add repr method to row.data.get() to precise the datatype
            ) + " |"
            for row in self.tuples
        ]

        return "\n".join([border, header, border] + data_tuples + [border])

    

    def display(self) -> None: 
        print(self)

