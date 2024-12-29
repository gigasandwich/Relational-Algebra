from ..constraint.constraint import *  # Import all constraints from a single file
from ..base.domain import Domain
from ..base.column import Column
from ..base.relation import Relation

def main():
    """
    Main function to define columns and relations, insert data, and perform operations
    such as projection, selection, and joining on the defined relations.
    
    This function sets up two relations: Person and PersonDetails, each with their respective
    columns and constraints.
    """

    # ====================================================
    # Column Definitions
    # ====================================================

    # Columns of the first relation (Person) 

    col1 = Column(
        name="id", 
        domain=Domain(
            allowed_values=[1, 2, 3, 4], 
            allowed_types=[str], 
            constraints=[StringLengthConstraint(1, 2)]
        )
    )
    
    col2 = Column(
        name="name", 
        domain=Domain(
            allowed_values=["Pupuce", "Japon", "Bocdom", "Stove", "Poyz", "Salohy"], 
            constraints=[StringLengthConstraint(1, 6)]
        )
    )
    
    # Columns of the second relation (PersonDetails) 

    col3 = Column(
        name="id", 
        domain=Domain(
            allowed_types=[int, str]
        )
    )
    
    col4 = Column(
        name="age", 
        domain=Domain(
            allowed_types=[int], 
            constraints=[PositiveConstraint(32)]
        )
    )

    # ====================================================
    # Relation Definitions
    # ====================================================

    # First relation
    person = Relation("Person", col1, col2)
    person.insert("id", 1, "name", "Pupuce")  # Valid insertion
    """person.insert("id", 2, "name", "RAKOTOBE")  # Should raise an exception due to name length = 8 > 6"""
    person.insert("id", 3, "name", "Japon")  # Valid insertion
    person.insert("id", "20", "name", "Salohy")  # Valid insertion (id as string)

    # Second relation
    person_details = Relation("PersonDetails", col3, col4)
    person_details.insert("id", 1, "age", 16)  # Valid insertion
    """person_details.insert("id", 2, "age", 38)  # Should raise an exception due to age > 32"""
    person_details.insert("id", 3, "age", 20)  # Valid insertion
    person_details.insert("id", 100, "age", 20)  # Should raise an exception (id not in Person relation)
    person_details.insert("id", "20", "age", 32)  # Valid insertion (id as string)

    # ====================================================
    # Relation Methods Definitions
    # ====================================================
    
    # Display the contents of the Person relation
    person.display()  
    
    # Perform projection operation to display only the 'id' column
    person.project("id").display()


if __name__ == "__main__":
    main()
