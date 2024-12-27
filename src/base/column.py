from .domain import Domain

class Column:
    """
    The main components of a relation
    It has a name and a domain
    """

    # ====================================================
    # Initialisation Method
    # ====================================================

    def __init__(self, name: str, domain: "Domain" = Domain(allowed_types = [object])):
        """
        If there's no domain added, by default the domain will be composed of any object

        Args:
            name (str): The name which we will identify the column from others in a relation
            domain (Domain): The domain object which the future rows will follow its rules 

        Raises:
            ValueError: if the specified domain is literally None
        """
        self.name = name
        self.domain = domain
        if domain is None:
            raise ValueError("A column must have a domain")

    # ====================================================
    # Main Methods
    # ====================================================
