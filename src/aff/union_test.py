from ..constraint.constraint import *  # Import all constraints from a single file
from ..base.domain import Domain
from ..base.column import Field
from ..base.relation import Relation

def main():
    """
    Main function to define columns and relations, insert data, and perform operations
    such as projection, selection, and joining on the defined relations.
    
    This function sets up two relations: Relation1 and Relation2, each with their respective
    columns and constraints.
    """

    # ====================================================
    # Domain Definitions
    # ====================================================
    domain1 = Domain(allowed_values=[1, 2, 3], allowed_types=[int], constraints=[RangeConstraint(1, 5)])
    domain2 = Domain(allowed_values=[2, 3, 4], allowed_types=[int], constraints=[RangeConstraint(2, 6)])

    # Create fields with the domains
    field1 = Field("id", domain1)
    field2 = Field("id", domain2)

    # ====================================================
    # Relation Definitions
    # ====================================================
    relation1 = Relation("Relation1", field1)
    relation2 = Relation("Relation2", field2)

    # Insert data into the relations
    relation1.insert("id", 1)  # Valid insertion based on domain1
    relation1.insert("id", 2)  # Valid insertion based on domain1
    relation1.insert("id", 3)  # Valid insertion based on domain1

    relation1.insert("id", 6)  # Will fail due to domain constraints (RangeConstraint(1, 5))

    relation2.insert("id", 2)  # Valid insertion based on domain2
    relation2.insert("id", 3)  # Valid insertion based on domain2
    relation2.insert("id", 4)  # Valid insertion based on domain2

    # ====================================================
    # Display the Domains of Each Relation
    # ====================================================
    print("Domain of Relation1:")
    for field in relation1.fields:
        print(f"Field: {field.name}, Domain: {field.domain}")

    print("\nDomain of Relation2:")
    for field in relation2.fields:
        print(f"Field: {field.name}, Domain: {field.domain}")

    # ====================================================
    # Field Mapping for Union, Intersection, and Difference
    # ====================================================
    field_mapping = {"id": "id"}

    # ====================================================
    # Perform Union, Intersection, and Difference
    # ====================================================
    print("\n=== Union of Relation1 and Relation2 ===")
    union_result = relation1.union(relation2, field_mapping)
    union_result.display()

    # Display the domain of the union result
    print("\nDomain of Union Result:")
    for field in union_result.fields:
        print(f"Field: {field.name}, Domain: {field.domain}")

    print("\n=== Intersection of Relation1 and Relation2 ===")
    intersection_result = relation1.intersection(relation2, field_mapping)
    intersection_result.display()

    # Display the domain of the intersection result
    print("\nDomain of Intersection Result:")
    for field in intersection_result.fields:
        print(f"Field: {field.name}, Domain: {field.domain}")

    print("\n=== Difference of Relation1 and Relation2 ===")
    difference_result = relation1.difference(relation2, field_mapping)
    difference_result.display()

    # Display the domain of the difference result
    print("\nDomain of Difference Result:")
    for field in difference_result.fields:
        print(f"Field: {field.name}, Domain: {field.domain}")


if __name__ == "__main__":
    main()
