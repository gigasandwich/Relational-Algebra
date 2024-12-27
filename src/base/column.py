from .domain import Domain

class Column:
    """
    The main components of a relation
    It has a name and a domain
    """

    # ====================================================
    # Initialisation Method
    # ====================================================

    def __init__(self, name: str, domain: "Domain" = Domain(allowed_types = (object)), allowed_types=None, allowed_values=None, constraints=None):
        """
        If there's no domain added, by default the domain will be composed of any object

        Args:
            name (str): The name which we will identify the column from others in a relation
            domain (Domain): The domain object which the future rows will follow its rules 
            All the other arguments of a domain object constructor (optionals)

        Raises:
            ValueError: if the specified domain is literally None
        """
        self.name = name
        self.domain = domain if domain is not None else Domain(allowed_types, allowed_values, constraints)

        if domain is None:
            raise ValueError("A column must have a domain")

    # ====================================================
    # Main Methods
    # ====================================================
    
    def is_valid(self, value: object) -> bool:
        return self.domain.is_valid(value)
    
    def union(self, other_column):
        domain = self.domain.union(other_column.domain)
        new_name = f"{self.name}|{other_column.name}"
        return Column(new_name, domain)
    
    def intersection(self, other_column):
        domain = self.domain.intersection(other_column.domain)
        new_name = f"{self.name}|{other_column.name}"
        return Column(new_name, domain)
    
    # ====================================================
    # Display Methods
    # ====================================================

    def __str__(self):
        return f"Column(name={self.name}, domain={self.domain})"

    def display(self):
        print(self)