from ..constraint.constraint import *  # Import all constraints from a single file
from ..base.domain import Domain
from ..base.column import Field
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

    # Fields of the first relation (Person) 

    field1 = Field(
        name="id", 
        domain=Domain(
            allowed_values=[1, 2, 3, 4], 
            allowed_types=[str], 
            constraints=[StringLengthConstraint(1, 2)]
        )
    )
    
    field2 = Field(
        name="name", 
        domain=Domain(
            allowed_values=["Pupuce", "Japon", "Bocdom", "Stove", "Poyz", "Salohy", "RAKOTO"], 
            constraints=[StringLengthConstraint(1, 6)]
        )
    )
    
    # Fields of the second relation (PersonDetails) 

    field3 = Field(
        name="id", 
        domain=Domain(
            allowed_types=[int, str]
        )
    )
    
    field4 = Field(
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
    person = Relation("Person", field1, field2)
    person.insert("id", 1, "name", "Pupuce")  # Valid insertion
    person.insert("id", 2, "name", "RAKOTO")  # If name = RAKOTOBE: Should raise an exception due to name length = 8 > 6
    person.insert("id", 3, "name", "Japon")  # Valid insertion
    person.insert("id", "20", "name", "Salohy")  # Valid insertion (id as string)

    # Second relation
    person_details = Relation("PersonDetails", field3, field4)
    person_details.insert("id", 1, "age", 16)  # Valid insertion
    person_details.insert("id", 3, "age", 20)  # Valid insertion
    person_details.insert("id", "20", "age", 32)  # Valid insertion (id as string)
    person_details.insert("id", 100, "age", 20)  # id not in Person relation
    person_details.insert("id", 200, "age", 18)  # If age = 38: Should raise an exception due to age > 32

    # ====================================================
    # Relation main methods
    # ====================================================
    
    # First look at person relation
    person.display()  
    person_details.display()

    # Conditions for the selection method 
    condition1 = 'id <= 3'
    condition2 = '(id == "20" or name == "Pupuce") and (name == "Salohy")'
    condition3 = "Person.id == PersonDetails.id"
    
    # Relation main methods
    # person.project("*").display()
    # person.select(condition2).display()

    # Join methods
    # join = person.cartesian_product(person_details)
    # join = person.automatic_natural_join(person_details)
    # join = person.natural_join(person_details, "id", "id")
    # join = person.theta_join(person_details, condition3)
    # join = person.equi_join(person_details, "id", "id")
    # join.display()

    # Outer join methods
    # outer_join = person.outer_join(person_details, condition3)
    # outer_join = person.left_outer_join(person_details, condition3)
    # outer_join = person.right_outer_join(person_details, condition3)
    # outer_join.display()


if __name__ == "__main__":
    main()
