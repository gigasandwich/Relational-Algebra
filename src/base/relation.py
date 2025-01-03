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
        new_relation.name = f"{self.name} PROJECTED {col_names}"
        
            

        # Step 1: Regrouping the Column objects that are requested
        needed_cols = []

        if "*" in col_names:
            col_names = set(col_names)
            col_names = (field.name for field in self.fields)

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
        new_relation = Relation(f"{copy.name} WHERE: {condition}", *copy.fields)
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
        new_relation.name = self.name + " THETA JOIN "  + other.name
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
        new_relation.name = f"{self.name} NATURAL JOIN {other.name}: {common_fields}"

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
        new_relation = Relation(f"{self.name} NATURAL JOIN {other.name}")
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
    # TODO: Arg of add_unmatched_rows: not theta_join but condition of the theta_join, but it destroys the logic of the algorithm

    def outer_join(self, other: "Relation", condition: str) -> "Relation":
        theta_join = self.theta_join(other, condition)
        
        # Using these so that there's automaticaly a prefix before column names
        self_relation = self.copy_with_renamed_fields(self.name)
        other_relation = other.copy_with_renamed_fields(other.name)

        result_relation = Relation(f"{self.name} FULL OUTER JOIN {other.name}")
        result_relation.fields = self_relation.fields + other_relation.fields  
        result_relation.tuples.extend(theta_join.tuples)

        # Handle unmatched rows from both sides
        result_relation.add_unmatched_rows(self_relation, other_relation, theta_join)
        result_relation.add_unmatched_rows(other_relation, self_relation, theta_join)
        return result_relation

    def left_outer_join(self, other: "Relation", condition: str) -> "Relation":
        theta_join = self.theta_join(other, condition)
        
        self_relation = self.copy_with_renamed_fields(self.name)
        other_relation = other.copy_with_renamed_fields(other.name)

        result_relation = Relation(f"{self.name} LEFT OUTER JOIN {other.name}")
        result_relation.fields = self_relation.fields + other_relation.fields
        result_relation.tuples.extend(theta_join.tuples)

        # Handle unmatched rows from the left side only
        result_relation.add_unmatched_rows(self_relation, other_relation, theta_join)
        return result_relation

    def right_outer_join(self, other: "Relation", condition: str) -> "Relation":
        """
        Performs a right outer join between two relations based on a condition.
        """
        theta_join = self.theta_join(other, condition)
        
        self_relation = self.copy_with_renamed_fields(self.name)
        other_relation = other.copy_with_renamed_fields(other.name)

        result_relation = Relation(f"{self.name} LEFT OUTER JOIN {other.name}")
        result_relation.fields = self_relation.fields + other_relation.fields
        result_relation.tuples.extend(theta_join.tuples)

        # Handle unmatched rows from the left side only
        result_relation.add_unmatched_rows(other_relation, self_relation, theta_join)
        return result_relation
    

    # ====================================================
    # Union - Intersection - Difference Methods
    # ====================================================
    
    def union(self, other: "Relation", field_mapping: dict) -> "Relation":
        """
        Performs a union operation on two relations using the specified field mapping.
        The result only includes fields specified in the field_mapping.
        """
        # Validate field_mapping
        for self_field, other_field in field_mapping.items():
            if self_field not in [f.name for f in self.fields]:
                raise ValueError(f"Field '{self_field}' not found in '{self.name}'.")
            if other_field not in [f.name for f in other.fields]:
                raise ValueError(f"Field '{other_field}' not found in '{other.name}'.")

        # Create a new relation with fields specified in field_mapping
        result_fields = [
            Field(name, self.get_field_by_name(name).domain.union(other.get_field_by_name(field_mapping[name]).domain))
            for name in field_mapping.keys()
        ]
        new_relation = Relation(f"{self.name}_UNION_{other.name}", *result_fields)

        # Helper to construct tuples based on field_mapping
        def construct_tuple(source_relation, row, field_mapping):
            new_tuple = Tuple(new_relation)
            for self_field, other_field in field_mapping.items():
                new_tuple.data[self_field] = row.data[other_field]
            return new_tuple

        # Add tuples from both relations, ensuring no duplicates
        added_tuples = set()  # Keep track of added tuples for deduplication
        for row in self.tuples:
            new_tuple = construct_tuple(self, row, field_mapping)
            tuple_key = tuple(new_tuple.data.values())  # Generate a hashable key for deduplication
            if tuple_key not in added_tuples:
                new_relation.add_tuple(new_tuple)
                added_tuples.add(tuple_key)

        for row in other.tuples:
            new_tuple = construct_tuple(other, row, field_mapping)
            tuple_key = tuple(new_tuple.data.values())  # Generate a hashable key for deduplication
            if tuple_key not in added_tuples:
                new_relation.add_tuple(new_tuple)
                added_tuples.add(tuple_key)

        return new_relation


    def intersection(self, other: "Relation", field_mapping: dict) -> "Relation":
        """
        Performs an intersection operation on two relations using the specified field mapping.
        The result only includes fields specified in the field_mapping.
        """
        # Validate field_mapping
        for self_field, other_field in field_mapping.items():
            if self_field not in [f.name for f in self.fields]:
                raise ValueError(f"Field '{self_field}' not found in '{self.name}'.")
            if other_field not in [f.name for f in other.fields]:
                raise ValueError(f"Field '{other_field}' not found in '{other.name}'.")

        # Create a new relation with fields specified in field_mapping
        result_fields = [
            Field(name, self.get_field_by_name(name).domain.intersection(other.get_field_by_name(field_mapping[name]).domain))
            for name in field_mapping.keys()
        ]
        new_relation = Relation(f"{self.name}_INTERSECTION_{other.name}", *result_fields)

        # Helper to construct tuples based on field_mapping
        def construct_tuple(source_relation, row, field_mapping):
            new_tuple = Tuple(new_relation)
            for self_field, other_field in field_mapping.items():
                new_tuple.data[self_field] = row.data[other_field]
            return new_tuple

        # Add tuples that exist in both relations
        other_tuples_set = {
            tuple(construct_tuple(other, row, field_mapping).data.values()) for row in other.tuples
        }

        for row in self.tuples:
            new_tuple = construct_tuple(self, row, field_mapping)
            tuple_key = tuple(new_tuple.data.values())
            if tuple_key in other_tuples_set:
                new_relation.add_tuple(new_tuple)

        return new_relation


    def difference(self, other: "Relation", field_mapping: dict) -> "Relation":
        """
        Performs a difference operation (self - other) on two relations using the specified field mapping.
        The result only includes fields specified in the field_mapping.
        """
        # Validate field_mapping
        for self_field, other_field in field_mapping.items():
            if self_field not in [f.name for f in self.fields]:
                raise ValueError(f"Field '{self_field}' not found in '{self.name}'.")
            if other_field not in [f.name for f in other.fields]:
                raise ValueError(f"Field '{other_field}' not found in '{other.name}'.")

        # Create a new relation with fields specified in field_mapping
        result_fields = [
            Field(name, self.get_field_by_name(name).domain.difference(other.get_field_by_name(field_mapping[name]).domain))
            for name in field_mapping.keys()
        ]
        new_relation = Relation(f"{self.name}_DIFFERENCE_{other.name}", *result_fields)

        # Helper to construct tuples based on field_mapping
        def construct_tuple(source_relation, row, field_mapping):
            new_tuple = Tuple(new_relation)
            for self_field, other_field in field_mapping.items():
                new_tuple.data[self_field] = row.data[other_field]
            return new_tuple

        # Add tuples that exist in self but not in other
        other_tuples_set = {
            tuple(construct_tuple(other, row, field_mapping).data.values()) for row in other.tuples
        }

        for row in self.tuples:
            new_tuple = construct_tuple(self, row, field_mapping)
            tuple_key = tuple(new_tuple.data.values())
            if tuple_key not in other_tuples_set:
                new_relation.add_tuple(new_tuple)

        return new_relation



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
        
        for tuple in self.tuples:
            new_tuple = tuple.copy()
            for field in self.fields:
                old_field_name = field.name
                new_field_name = prefix + "." + field.name
                new_tuple.data[new_field_name] = new_tuple.data.pop(old_field_name)

            new_relation.add_tuple(new_tuple)

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
    
    def add_unmatched_rows(self, primary_relation, secondary_relation, theta_join):
        """
        Adds unmatched rows from one relation (primary_relation) to self.
        Sets None for the fields from the secondary_relation.
        """
        unmatched_rows = []

        for row in primary_relation.tuples:
            matched = False
            # Check if the row matches any row in theta_join
            for matched_row in theta_join.tuples:
                if all(
                    row.data[field.name] == matched_row.data[field.name]
                    for field in primary_relation.fields
                ):
                    matched = True
                    break  

            # If no match was found, add to unmatched_rows
            if not matched:
                unmatched_rows.append(row)

        # Process unmatched rows
        for row in unmatched_rows:
            new_row = Tuple(self)

            for field in primary_relation.fields:
                new_row.data[field.name] = row.data[field.name]
            for field in secondary_relation.fields:
                new_row.data[field.name] = None

            self.add_tuple(new_row)


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
                (len(repr(str(tuple.data.get(field_name, "")))) for tuple in self.tuples), # Add repr method to tuple.data.get() to precise the datatype
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
                str(repr(tuple.data.get(field, ""))).ljust(width) for field, width in zip(field_names, field_widths) 
            ) + " |"
            for tuple in self.tuples
        ]

        return "\n".join([border, header, border] + data_tuples + [border])

    

    def display(self) -> None: 
        print(self)

