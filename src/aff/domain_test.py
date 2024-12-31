from ..constraint.constraint import *  # Import all constraints from a single file
from ..base.domain import Domain
from ..base.column import Field
from ..base.relation import Relation

domain1 = Domain(
    allowed_values=[1, 2, 3],
    allowed_types=[int],
    constraints=[RangeConstraint(1, 5), PositiveConstraint()]
)

domain2 = Domain(
    allowed_values=[2, 3, 4],
    allowed_types=[int],
    constraints=[RangeConstraint(3, 6)]
)

print(f"Domain1: {domain1}")
print(f"Domain2: {domain2}")

# Union
union_domain = domain1.union(domain2)
print(f"Union Domain: {union_domain}")

# Intersection
intersection_domain = domain1.intersection(domain2)
print(f"Intersection Domain: {intersection_domain}")

# Difference
difference_domain = domain1.difference(domain2)
print(f"Difference Domain: {difference_domain}")
