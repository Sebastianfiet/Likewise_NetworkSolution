class Link:
    """
    A class to represent a network link between two nodes.

    Attributes:
    - source (int): The ID of the source node.
    - destination (int): The ID of the destination node.
    - bandwidth (int): The bandwidth of the link in Gbps.

    Methods:
    - __init__(self, source, destination, bandwidth): Initializes a Link object with the given attributes.
    - __repr__(self): Returns a string representation of the Link object.
    """

    def __init__(self, source, destination, bandwidth):
        """
        Initializes a Link object with the given attributes.

        Parameters:
        - source (int): The ID of the source node.
        - destination (int): The ID of the destination node.
        - bandwidth (int): The bandwidth of the link in Gbps.
        """
        self.source = source
        self.destination = destination
        self.bandwidth = bandwidth

    def __repr__(self):
        """
        Returns a string representation of the Link object.

        Returns:
        - str: A string representing the Link object.
        """
        return f"Link({self.source} -> {self.destination}, Bandwidth={self.bandwidth} Gbps)"
